import gizmo
from subsync import subtitle
from subsync.synchro import pipeline, dictionary, encdetect, wordsdump, controller
import threading

import logging
logger = logging.getLogger(__name__)


class Synchronizer(object):
    def __init__(self, sub, ref):
        self.sub = sub
        self.ref = ref

        self.onUpdate = lambda: None
        self.onError = lambda src, err: None

        self.stats = gizmo.CorrelationStats()
        self.effortBegin = None
        self.statsLock = threading.Lock()

        self.correlator = None
        self.translator = None
        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []
        self.wordsDumpers = []

    def destroy(self):
        logger.info('releasing synchronizer resources')

        if self.correlator:
            self.correlator.stop(force=True)

        for p in self.pipelines:
            p.stop()

        for p in self.pipelines:
            p.destroy()

        if self.correlator:
            self.correlator.wait()
            self.correlator.connectStatsCallback(None)

        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []
        self.translator = None
        self.dictionary = None
        self.refWordsSink = None

        for wd in self.wordsDumpers:
            wd.flush()

        self.wordsDumpers = []

    def init(self, options, runCb=None):
        try:
            self._initInternal(options, runCb)
        except gizmo.ErrorTerminated:
            logger.info('initialization terminated')

    def _initInternal(self, options, runCb=None):
        logger.info('initializing synchronization jobs')
        for stream in (self.sub, self.ref):
            if stream.type == 'subtitle/text' and not stream.enc and len(stream.streams) == 1:
                stream.enc = encdetect.detectEncoding(stream.path, stream.lang)

        self.correlator = gizmo.Correlator(
                options['windowSize'],
                options['minCorrelation'],
                options['maxPointDist'],
                options['minPointsNo'],
                options['minWordsSim'])
        self.correlator.connectStatsCallback(self.onStatsUpdate)
        self.refWordsSink = self.correlator.pushRefWord
        self.subtitlesCollector = subtitle.SubtitlesCollector()

        self.subPipeline = pipeline.createProducerPipeline(self.sub)
        self.subPipeline.connectEosCallback(self.onSubEos)
        self.subPipeline.connectErrorCallback(self.onSubError)
        self.subPipeline.addSubsListener(self.subtitlesCollector.addSubtitle)
        self.subPipeline.addSubsListener(self.correlator.pushSubtitle)
        self.subPipeline.addWordsListener(self.correlator.pushSubWord)

        if self.sub.lang and self.ref.lang and self.sub.lang != self.ref.lang:
            self.dictionary = dictionary.loadDictionary(self.ref.lang, self.sub.lang, options['minWordLen'])
            self.translator = gizmo.Translator(self.dictionary)
            self.translator.setMinWordsSim(options['minWordsSim'])
            self.translator.addWordsListener(self.correlator.pushRefWord)
            self.refWordsSink = self.translator.pushWord

        self.refPipelines = pipeline.createProducerPipelines(self.ref, no=options['jobsNo'], runCb=runCb)

        for p in self.refPipelines:
            p.connectEosCallback(self.onRefEos)
            p.connectErrorCallback(self.onRefError)
            p.addWordsListener(self.refWordsSink)

        self.pipelines = [ self.subPipeline ] + self.refPipelines

        for p in self.pipelines:
            p.configure(
                    minWordLen=options['minWordLen'],
                    minWordProb=options['minWordProb'])

        dumpSources = {
                'sub':     [ self.subPipeline ],
                'subPipe': [ self.subPipeline ],
                'subRaw':  [ self.subPipeline.getRawWordsSource() ],
                'ref':     [ self.translator ] if self.translator else self.refPipelines,
                'refPipe': self.refPipelines,
                'refRaw':  [ p.getRawWordsSource() for p in self.refPipelines ],
                }

        for srcId, path in options.get('dumpWords', []):
            sources = dumpSources.get(srcId)
            if sources:
                logger.debug('dumping %s to %s (from %i sources)', srcId, path, len(sources))
                if path:
                    wd = wordsdump.WordsFileDump(path, overwrite=True)
                else:
                    wd = wordsdump.WordsStdoutDump(srcId)
                self.wordsDumpers.append(wd)
                for source in sources:
                    source.addWordsListener(wd.pushWord)

    def start(self):
        logger.info('starting synchronization')
        self.correlator.start('Correlator')
        for id, p in enumerate(self.pipelines):
            p.start('Pipeline{}'.format(id))

    def stop(self, force=True):
        logger.info('stopping synchronizer')
        self.correlator.stop(force=force)

        for p in self.pipelines:
            p.stop()

    def isRunning(self):
        if self.correlator and self.correlator.isRunning():
            return True

        for p in self.pipelines:
            if p.isRunning():
                return True

        return False

    def getProgress(self):
        psum = 0.0
        plen = 0

        for pr in  [ p.getProgress() for p in self.pipelines ]:
            if pr != None:
                psum += pr
                plen += 1

        if self.correlator:
            cp = self.correlator.getProgress()
            res = cp * cp
        else:
            res = 0.0

        if plen > 0:
            res *= psum / plen

        if res < 0: res = 0
        if res > 1: res = 1
        return res

    def getStatus(self):
        with self.statsLock:
            stats = self.stats
            progress = self.getProgress()
            begin = self.effortBegin

        effort = -1
        if begin is not None and begin < 1.0:
            if progress <= 0.0:
                effort = 0.0
            elif progress >= 1.0:
                effort = 1.0
            else:
                effort = (progress - begin) / (1.0 - begin)

        return controller.SyncStatus(
                correlated  = stats.correlated and self.subPipeline and not self.subPipeline.isRunning(),
                maxChange   = self.subtitlesCollector.getMaxSubtitleDiff(stats.formula),
                progress    = progress,
                factor      = stats.factor,
                points      = stats.points,
                formula     = stats.formula,
                effort      = effort)

    def getSynchronizedSubtitles(self):
        with self.statsLock:
            formula = self.stats.formula
        return self.subtitlesCollector.getSynchronizedSubtitles(formula)

    def onStatsUpdate(self, stats):
        logger.debug(stats)
        with self.statsLock:
            self.stats = stats
            if self.effortBegin == None and stats.correlated and self.subPipeline and not self.subPipeline.isRunning():
                self.effortBegin = self.getProgress()
        self.onUpdate()

    def onSubEos(self):
        logger.info('subtitles read done')
        self.checkIfAllPipelinesDone()
        with self.statsLock:
            if self.effortBegin == None and self.stats.correlated:
                self.effortBegin = self.getProgress()

    def onRefEos(self):
        logger.info('references read done')
        self.checkIfAllPipelinesDone()

    def checkIfAllPipelinesDone(self):
        for p in self.pipelines:
            if p.isRunning():
                return
        logger.info('stopping correlator')
        self.correlator.stop(force=False)
        self.onUpdate()

    def onSubError(self, err):
        logger.warning('SUB: %r', str(err).replace('\n', '; '))
        self.onError('sub', err)

    def onRefError(self, err):
        logger.warning('REF: %r', str(err).replace('\n', '; '))
        self.onError('ref', err)

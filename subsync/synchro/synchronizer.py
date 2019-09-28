import gizmo
from subsync import subtitle
from subsync.settings import settings
from subsync.synchro import pipeline, dictionary, encdetect, wordsdump
import threading
import multiprocessing
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)


def getJobsNo():
    no = settings().jobsNo
    if type(no) is int and no >= 1:
        return no
    else:
        return max(multiprocessing.cpu_count(), 2)


SyncStatus = namedtuple('SyncStatus', [
    'subReady',
    'running',
    'maxChange',
    'progress',
    'correlated',
    'factor',
    'points',
    'maxDistance',
    'formula',
    'effort',
])


class Synchronizer(object):
    def __init__(self, sub, ref):
        self.sub = sub
        self.ref = ref

        self.onError = lambda src, err: None

        self.correlator = gizmo.Correlator(
                settings().windowSize,
                settings().minCorrelation,
                settings().maxPointDist,
                settings().minPointsNo,
                settings().minWordsSim)
        self.correlator.connectStatsCallback(self.onStatsUpdate)
        self.refWordsSink = self.correlator.pushRefWord
        self.subtitlesCollector = subtitle.SubtitlesCollector()

        self.stats = gizmo.CorrelationStats()
        self.effortBegin = None
        self.statsLock = threading.Lock()

        self.translator = None
        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []
        self.wordsDumpers = []

    def destroy(self):
        logger.info('releasing synchronizer resources')

        self.correlator.connectStatsCallback(None)

        for p in self.pipelines:
            p.destroy()

        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []
        self.translator = None
        self.refWordsSink = None

        for wd in self.wordsDumpers:
            wd.flush()

        self.wordsDumpers = []

    def init(self, runCb=lambda: True):
        logger.info('initializing synchronization jobs')
        for stream in (self.sub, self.ref):
            if stream.type == 'subtitle/text' and not stream.enc and len(stream.streams) == 1:
                stream.enc = encdetect.detectEncoding(stream.path, stream.lang)

        if not runCb():
            return

        self.subPipeline = pipeline.createProducerPipeline(self.sub)
        self.subPipeline.connectEosCallback(self.onSubEos)
        self.subPipeline.connectErrorCallback(self.onSubError)
        self.subPipeline.addSubsListener(self.subtitlesCollector.addSubtitle)
        self.subPipeline.addWordsListener(self.correlator.pushSubWord)

        if not runCb():
            return

        if self.sub.lang and self.ref.lang and self.sub.lang != self.ref.lang:
            self.dictionary = dictionary.loadDictionary(self.ref.lang, self.sub.lang, settings().minWordLen)
            self.translator = gizmo.Translator(self.dictionary)
            self.translator.setMinWordsSim(settings().minWordsSim)
            self.translator.addWordsListener(self.correlator.pushRefWord)
            self.refWordsSink = self.translator.pushWord

        if not runCb():
            return

        self.refPipelines = pipeline.createProducerPipelines(self.ref, no=getJobsNo(), runCb=runCb)

        for p in self.refPipelines:
            p.connectEosCallback(self.onRefEos)
            p.connectErrorCallback(self.onRefError)
            p.addWordsListener(self.refWordsSink)

        self.pipelines = [ self.subPipeline ] + self.refPipelines

        dumpSources = {
                'sub':     [ self.subPipeline ],
                'subPipe': [ self.subPipeline ],
                'subRaw':  [ self.subPipeline.getRawWordsSource() ],
                'ref':     [ self.translator ] if self.translator else self.refPipelines,
                'refPipe': self.refPipelines,
                'refRaw':  [ p.getRawWordsSource() for p in self.refPipelines ],
                }

        for srcId, path in settings().dumpWords:
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
        if self.correlator.isRunning():
            return True

        for p in self.pipelines:
            if p.isRunning():
                return True

        return False

    def isSubReady(self):
        with self.statsLock:
            return self.subPipeline and self.subPipeline.done and self.stats.correlated

    def getProgress(self):
        psum = 0.0
        plen = 0

        for pr in  [ p.getProgress() for p in self.pipelines ]:
            if pr != None:
                psum += pr
                plen += 1

        cp = self.correlator.getProgress()
        res = cp * cp

        if plen > 0:
            res *= psum / plen

        if res < 0: res = 0
        if res > 1: res = 1
        return res

    def getStatus(self):
        with self.statsLock:
            stats = self.stats
            progress = self.getProgress()

        return SyncStatus(
                subReady    = self.subPipeline and self.subPipeline.done and self.stats.correlated,
                running     = self.isRunning(),
                maxChange   = self.subtitlesCollector.getMaxSubtitleDiff(stats.formula),
                progress    = progress,
                correlated  = self.stats.correlated,
                factor      = self.stats.factor,
                points      = self.stats.points,
                maxDistance = self.stats.maxDistance,
                formula     = self.stats.formula,
                effort      = self.getEffort(progress))

    def getEffort(self, progress=None):
        with self.statsLock:
            begin = self.effortBegin
        if begin == None:
            return -1
        if progress == None:
            progress = self.getProgress()
        if progress == None or progress <= 0:
            return 0
        if progress >= 1:
            return 1
        return (progress - begin) / (1 - begin)

    def getSynchronizedSubtitles(self):
        with self.statsLock:
            formula = self.stats.formula
        return self.subtitlesCollector.getSynchronizedSubtitles(formula)

    def onStatsUpdate(self, stats):
        logger.debug(stats)
        with self.statsLock:
            self.stats = stats
            if self.effortBegin == None and self.subPipeline and self.subPipeline.done and stats.correlated:
                self.effortBegin = self.getProgress()

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
            if not p.done:
                return
        self.correlator.stop(force=False)

    def onSubError(self, err):
        logger.warning('SUB: %r', str(err).replace('\n', '; '))
        self.onError('sub', err)

    def onRefError(self, err):
        logger.warning('REF: %r', str(err).replace('\n', '; '))
        self.onError('ref', err)

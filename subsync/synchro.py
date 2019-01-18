import gizmo
from subsync import pipeline
from subsync import subtitle
from subsync.settings import settings
from subsync import dictionary
from subsync import encdetect
import threading
import multiprocessing

import logging
logger = logging.getLogger(__name__)


def getJobsNo():
    no = settings().jobsNo
    if type(no) is int and no >= 1:
        return no
    else:
        return max(multiprocessing.cpu_count(), 2)


class Synchronizer(object):
    def __init__(self, listener, subs, refs):
        self.listener = listener
        self.subs = subs
        self.refs = refs

        self.fps = refs.stream().frameRate
        if self.fps == None:
            self.fps = refs.fps

        self.correlator = gizmo.Correlator(
                settings().windowSize,
                settings().minCorrelation,
                settings().maxPointDist,
                settings().minPointsNo,
                settings().minWordsSim)

        self.stats = gizmo.CorrelationStats()
        self.statsLock = threading.Lock()
        self.correlator.connectStatsCallback(self.onStatsUpdate)

        self.subtitlesCollector = subtitle.SubtitlesCollector()

        for stream in (subs, refs):
            if stream.type == 'subtitle/text' and not stream.enc and len(stream.streams) == 1:
                stream.enc = encdetect.detectEncoding(stream.path, stream.lang)

        self.subPipeline = pipeline.createProducerPipeline(subs)
        self.subPipeline.connectEosCallback(self.onSubEos)
        self.subPipeline.connectErrorCallback(self.onSubError)
        self.subPipeline.connectSubsCallback(self.subtitlesCollector.addSubtitle)

        if subs.lang and refs.lang and subs.lang != refs.lang:
            self.dictionary = dictionary.loadDictionary(subs.lang, refs.lang, settings().minWordLen)
            self.translator = gizmo.Translator(self.dictionary)
            self.translator.setMinWordsSim(settings().minWordsSim)
            self.subPipeline.connectWordsCallback(self.translator.pushWord)
            self.translator.connectWordsCallback(self.correlator.pushSubWord)
        else:
            self.subPipeline.connectWordsCallback(self.correlator.pushSubWord)

        self.refPipelines = pipeline.createProducerPipelines(refs, getJobsNo())
        for p in self.refPipelines:
            p.connectEosCallback(self.onRefEos)
            p.connectErrorCallback(self.onRefError)
            p.connectWordsCallback(self.correlator.pushRefWord)

        self.pipelines = [ self.subPipeline ] + self.refPipelines

    def destroy(self):
        self.stop()
        self.correlator.connectStatsCallback(None)

        for p in self.pipelines:
            p.destroy()

        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []

    def start(self):
        logger.info('starting synchronization jobs')
        self.correlator.start('Correlator')
        for id, p in enumerate(self.pipelines):
            p.start('Pipeline{}'.format(id))

    def stop(self):
        self.correlator.stop()
        for p in self.pipelines:
            p.stop()

    def isRunning(self):
        if self.correlator.isRunning() and not self.correlator.isDone():
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

        cp = self.correlator.getProgress()
        res = cp * cp

        if plen > 0:
            res *= psum / plen

        return res

    def getStats(self):
        with self.statsLock:
            return self.stats

    def getMaxChange(self):
        return self.subtitlesCollector.getMaxSubtitleDiff(self.getStats().formula)

    def getSynchronizedSubtitles(self):
        return self.subtitlesCollector.getSynchronizedSubtitles(self.getStats().formula)

    def onStatsUpdate(self, stats):
        logger.debug(stats)
        with self.statsLock:
            self.stats = stats

    def onSubError(self, err):
        logger.warning('SUB: %r', str(err).replace('\n', '; '))
        self.listener.onError('sub', err)
        if 'terminated' in err.fields:
            self.stop()

    def onRefError(self, err):
        logger.warning('REF: %r', str(err).replace('\n', '; '))
        self.listener.onError('ref', err)
        if 'terminated' in err.fields:
            self.stop()

    def onSubEos(self):
        logger.info('subtitle job terminated')
        self.listener.onSubReady()

    def onRefEos(self):
        logger.info('reference job terminated')

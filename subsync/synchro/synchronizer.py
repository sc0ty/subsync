import gizmo
from subsync.synchro import pipeline
from subsync import subtitle
from subsync.settings import settings
from subsync.synchro import dictionary
from subsync import encdetect
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

        self.refCache = None
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

        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []

    def onRefWord(self, word):
        self.refWordsSink(word)

        if self.refCache and self.refCache.id:
            self.refCache.data.append((word))

    def destroy(self):
        logger.info('releasing synchronizer resources')
        self.correlator.connectStatsCallback(None)

        for p in self.pipelines:
            p.destroy()

        self.subPipeline = None
        self.refPipelines = []
        self.pipelines = []

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
        self.subPipeline.connectSubsCallback(self.subtitlesCollector.addSubtitle)
        self.subPipeline.connectWordsCallback(self.correlator.pushSubWord)

        if not runCb():
            return

        if self.sub.lang and self.ref.lang and self.sub.lang != self.ref.lang:
            self.dictionary = dictionary.loadDictionary(self.ref.lang, self.sub.lang, settings().minWordLen)
            self.translator = gizmo.Translator(self.dictionary)
            self.translator.setMinWordsSim(settings().minWordsSim)
            self.translator.connectWordsCallback(self.correlator.pushRefWord)
            self.refWordsSink = self.translator.pushWord

        if not runCb():
            return

        if self.refCache and self.refCache.isValid(self.ref):
            logger.info('restoring cached reference words (%i)', len(self.refCache.data))

            for word in self.refCache.data:
                self.refWordsSink(word)

            self.refPipelines = pipeline.createProducerPipelines(self.ref, timeWindows=self.refCache.progress,
                    runCb=runCb)

        else:
            if self.refCache:
                self.refCache.init(self.ref)

            self.refPipelines = pipeline.createProducerPipelines(self.ref, no=getJobsNo(), runCb=runCb)

        for p in self.refPipelines:
            p.connectEosCallback(self.onRefEos)
            p.connectErrorCallback(self.onRefError)
            p.connectWordsCallback(self.onRefWord)

        self.pipelines = [ self.subPipeline ] + self.refPipelines

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

        if self.refCache and self.refCache.id and self.refPipelines:
            self.refCache.progress = [ (p.getPosition(), *p.timeWindow)
                    for p in self.refPipelines
                    if not p.done and p.getPosition() < p.timeWindow[1] ]

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

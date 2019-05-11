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
    def __init__(self, subs, refs, refsCache=None):
        self.subs = subs
        self.refs = refs
        self.refsCache = refsCache

        self.onError = lambda src, err: None

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
        self.subPipeline.connectErrorCallback(self.onSubError)
        self.subPipeline.connectSubsCallback(self.subtitlesCollector.addSubtitle)
        self.subPipeline.connectWordsCallback(self.correlator.pushSubWord)

        if subs.lang and refs.lang and subs.lang != refs.lang:
            self.dictionary = dictionary.loadDictionary(refs.lang, subs.lang, settings().minWordLen)
            self.translator = gizmo.Translator(self.dictionary)
            self.translator.setMinWordsSim(settings().minWordsSim)
            self.translator.connectWordsCallback(self.correlator.pushRefWord)
            self.refWordsSink = self.translator.pushWord
        else:
            self.refWordsSink = self.correlator.pushRefWord

        if refsCache and refsCache.isValid(self.refs):
            logger.info('restoring cached reference words (%i)', len(refsCache.data))

            for word in refsCache.data:
                self.refWordsSink(word)

            self.refPipelines = pipeline.createProducerPipelines(refs, timeWindows=refsCache.progress)

        else:
            if refsCache:
                refsCache.init(refs)

            self.refPipelines = pipeline.createProducerPipelines(refs, no=getJobsNo())

        for p in self.refPipelines:
            p.connectErrorCallback(self.onRefError)
            p.connectWordsCallback(self.onRefWord)

        self.pipelines = [ self.subPipeline ] + self.refPipelines

    def onRefWord(self, word):
        self.refWordsSink(word)

        if self.refsCache and self.refsCache.id:
            self.refsCache.data.append((word))

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

        if self.refsCache and self.refsCache.id:
            self.refsCache.progress = [ (p.getPosition(), *p.timeWindow)
                    for p in self.refPipelines
                    if not p.done and p.getPosition() < p.timeWindow[1] ]

    def isRunning(self):
        if self.correlator.isRunning() and not self.correlator.isDone():
            return True

        for p in self.pipelines:
            if p.isRunning():
                return True

        return False

    def isSubReady(self):
        with self.statsLock:
            return self.subPipeline.done and self.stats.correlated

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
        self.onError('sub', err)

    def onRefError(self, err):
        logger.warning('REF: %r', str(err).replace('\n', '; '))
        self.onError('ref', err)


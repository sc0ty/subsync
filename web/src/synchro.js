import { wrap } from 'comlink';
import webworkify from 'webworkify';
import Subtitles from './subtitle.js';
import settings from './settings.js';
import Logger from './logger.js';
const logger = Logger.logger.get('[Synchronizer]');

export default class Synchronizer {

  constructor() {
    this.correlator = wrap(webworkify(require('./correlator/worker.js')));
    this.subExtractor = wrap(webworkify(require('./extractor/worker.js')));
    this.refExtractors = [];
    this.extractors = [];
  }

  async getFileInfo(file) {
    const firstTime = await this.subExtractor.init(settings, 'SubExtractor')
    return await this.subExtractor.getFileInfo(file);
  }

  async run(sub, ref, listener) {
    this.running = true;
    this.progress = [];
    this.subtitles = new Subtitles();
    this.status = {};
    this.gotAllSubs = false;

    try {
      const refJobsNo = calcRefJobsNo(ref);
      this.progress = new Array(refJobsNo + 1).fill(0);
      for (let i = this.refExtractors.length; i < refJobsNo; i++) {
        this.refExtractors.push(wrap(webworkify(require('./extractor/worker.js'))));
      }

      const refExtractors = this.refExtractors.slice(0, refJobsNo);
      this.extractors = [ this.subExtractor, ...refExtractors ];

      await Promise.all([
        this.correlator.init(settings.serialize()),
        this.subExtractor.init(settings.serialize(), 'SubExtractor'),
        ...refExtractors.map((ex, i) => ex.init(settings.serialize(), `RefExtractor${i}`)),
      ]);

      if (await this.preloadAssets(sub, ref)) {
        await Promise.all(refExtractors.map(ex => ex.syncfs()));
      }

      await Promise.all([
        this.subExtractor.open(sub, { otherLang: ref.lang, postSubtitles: true }),
        ...refExtractors.map((ex, i) => ex.open(ref, {
          timeWindow: ref.duration && [ i * ref.duration / refJobsNo, (i + 1) * ref.duration / refJobsNo + 1 ]
        }))
      ]);

      listener.onSyncStarted();
      await Promise.all(this.extractors.map( (ex, i) => this.runExtractor(ex, i, listener)) );

    } finally {
      await Promise.all(this.extractors.map(ex => ex.close()));
      this.extractors = [];
    }
    return this.running;
  }

  stop() {
    this.running = false;
  }

  async runExtractor(extractor, no, listener) {
    const issub = extractor === this.subExtractor;
    const onNewWord = (issub ? this.addSubWord : this.addRefWord).bind(this);
    const onError = listener.onSyncError.bind(listener, issub ? 'sub' : 'ref');

    while (this.running) {
      try {
        const s = await extractor.run(2000);
        if (this.running && s.subtitles) {
          for (const sub of s.subtitles) {
            this.subtitles.addSubtitle(sub);
          }
          if (s.done) {
            this.gotAllSubs = true;
          }
          await this.correlator.addSubtitles(s.subtitles);
        }
        if (this.running && s.words) {
          const dp = ((s.progress || 0) - (this.progress[no] || 0)) * 2
            / (s.words.length * (s.words.length+1));

          for (const [i, word] of s.words.entries()) {
            this.progress[no] += dp * i;
            await onNewWord(word);
            if (!this.running) {
              break;
            }
          }
        }
        this.progress[no] = s.progress;
        if (s.done) {
          break;
        }

      } catch (e) {
        logger.error(issub ? 'subExtractor:' : `refExtractor${no - 1}:`, e);
        onError(e);
      }
    }
  }

  async preloadAssets(sub, ref) {
    const assets = [];
    if (sub.lang && ref.lang && sub.lang !== ref.lang) {
      assets.push({ type: 'dict', params: [sub.lang, ref.lang].sort() });
    }
    if (ref.type === 'audio') {
      assets.push({ type: 'speech', params: [ref.lang] });
    }
    if (assets.length) {
      logger.log('preloading assets', assets);
      await this.subExtractor.preloadAssets(assets);
      return true;
    }
  }

  async addSubWord(word) {
    const status = await this.correlator.addSubWord(word);
    if (status) {
      status.correlated = this.status.correlated || status.correlated;
      this.status = status;
    }
  }

  async addRefWord(word) {
    const status = await this.correlator.addRefWord(word);
    if (status) {
      status.correlated = this.status.correlated || status.correlated;
      this.status = status;
    }
  }

  getStatus() {
    return {
      ...this.status,
      subReady: this.status.correlated && this.gotAllSubs,
      progress: this.getProgress(),
      maxChange: this.subtitles.getMaxChange(this.status.formula),
    }
  }

  getProgress() {
    let progress = this.progress[0];
    const refs = this.progress.slice(1);
    if (refs.length) {
      const pr = refs.reduce((sum, pr) => sum + (pr || 0), 0) / refs.length;
      progress = Math.min(progress || 0, pr);
    }
    return progress || 0;
  }

  getSynchronizedSubtitles(format) {
    const formula = this.status.formula;
    if (formula) {
      return this.subtitles.getSynchronizedSubtitles(formula, format);
    }
  }
}

Synchronizer.instance = new Synchronizer();

function calcRefJobsNo(stream) {
  let jobsNo = settings.jobsNo || settings.defaultJobsNo;
  if (stream.duration == null) {
    jobsNo = 1;
  } else if (stream.duration / 60 < jobsNo) {
    jobsNo = Math.trunc(stream.duration / 60) || 1;
  }
  return jobsNo;
}

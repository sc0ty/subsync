import Logger from '../logger.js';
const logger = Logger.logger;

import { expose } from 'comlink';
import Gizmo from '../gizmowrap.js';
import settings from '../settings.js';

class Correlator {

  async init(newSettings, name) {
    if (name) {
      logger.setPrefix(`[${name}]`);
    }

    if (newSettings) {
      settings.assign(newSettings);
    }

    if (!Gizmo.instance) {
      await Gizmo.init(require('../../scripts/correlator.js'));
      logger.info('ready');
    }

    this.synchro = new Gizmo.instance.Synchronizer(
      settings.windowSize,
      settings.minCorrelation,
      settings.maxPointDist,
      settings.minPointsNo,
      settings.minWordsSim,
    );
  }

  addSubWord(w) {
    return this.synchro.addSubWord(w.time, w.duration, w.text);
  }

  addRefWord(w) {
    return this.synchro.addRefWord(w.time, w.duration, w.text);
  }

  addSubtitles(subtitles) {
    for (const s of subtitles) {
      this.synchro.addSubtitle(s.start, s.end);
    }
  }
}

export default function() {
  logger.setPrefix('[Correlator]');
  return expose(new Correlator());
}

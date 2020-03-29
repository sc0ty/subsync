import Logger from '../logger.js';
const logger = Logger.logger;

import { expose } from 'comlink';
import Gizmo from '../gizmowrap.js';
import Pipeline from './pipeline.js';
import Assets from './assets.js';
import Filesystem from './fs.js';
import settings from '../settings.js';

class Extractor {

  async init(newSettings, name) {
    try {
      if (name) {
        logger.setPrefix(`[${name}]`);
      }

      if (newSettings) {
        settings.assign(newSettings);
      }

      if (!Gizmo.instance) {
        await Gizmo.init(require('../../scripts/extractor.js'));
        const FS = Gizmo.instance.FS;
        FS.mkdir('/work');
        FS.mkdir('/assets');
        FS.mount(FS.filesystems.IDBFS, {}, '/assets');
        logger.info('ready');
        return true;
      }
    } catch (e) {
      handleException('init:', e);
    }
  }

  async preloadAssets(assets) {
    try {
      await Filesystem.syncfs(true);
      for (const asset of assets) {
        await Assets.preloadAsset(asset);
      }
      await Filesystem.syncfs(false);
    } catch (e) {
      handleException('preloadAssets:', e);
    }
  }

  async syncfs() {
    try {
      await Filesystem.syncfs(true);
    } catch (e) {
      handleException('syncfs:', e);
    }
  }

  async getFileInfo(file) {
    let pipeline = undefined;
    try {
      const path = this.mountFile(file);
      pipeline = new Pipeline(path);
      return {
        duration: pipeline.demux.getDuration(),
        streams: pipeline.streams,
      }

    } catch (e) {
      handleException('getFileInfo:', e);

    } finally {
      pipeline && pipeline.destroy();
      Gizmo.instance.FS.unmount('/work');
    }
  }

  async open(stream, params) {
    logger.log('open', stream);

    try {
      const path = this.mountFile(stream.file);
      this.pipeline = new Pipeline(path);
      this.timeWindow = params.timeWindow || [ 0, undefined ];
      this.words = [];
      this.subtitles = [];

      const output = this.pipeline.makePipeline(stream, params, path);
      output.addWordsListener( word => this.words.push(word) );

      if (params.postSubtitles) {
        this.pipeline.addSubsListener( subtitle => this.subtitles.push(subtitle) );
      }

      const demux = this.pipeline.demux;
      if (this.timeWindow[0]) {
        demux.seek(this.timeWindow[0]);
      }
      demux.start();

    } catch (e) {
      this.close();
      handleException('open:', e);
    }
  }

  async run(timeout) {
    try{
      const demux = this.pipeline.demux;
      const [ startTime, endTime ] = this.timeWindow;
      const ts = performance.now();
      const status = { progress: 1, done: true };

      while (demux.step() && (endTime == null || demux.getPosition() < endTime)) {
        if (timeout != null && (performance.now() - ts) >= timeout) {
          const num = demux.getPosition() - startTime;
          const den = (endTime || demux.getDuration()) - startTime;
          status.progress = den ? num/den : 0;
          status.done = false;
          break;
        }
      }

      if (this.words.length) {
        status.words = this.words;
        this.words = [];
      }
      if (this.subtitles.length) {
        status.subtitles = this.subtitles;
        this.subtitles = [];
      }

      status.done && logger.log('finished');
      return status;

    } catch (e) {
      handleException('run:', e);
    }
  }

  close() {
    logger.log('close');
    if (this.pipeline) {
      this.pipeline.destroy();
      this.pipeline = undefined;
      this.timeWindow = undefined;
      Gizmo.instance.FS.unmount('/work');
    }
  }

  mountFile(file) {
    const FS = Gizmo.instance.FS;
    FS.mount(FS.filesystems.WORKERFS, { files: [ file ] }, '/work');
    return '/work/' + file.name;
  }
}

function handleException(msg, err) {
  if (typeof err === 'number') {
    err = Gizmo.instance.getCurrentException() || err;
  } else if (!(err instanceof Error)) {
    err = Object.assign(new Error(), err, {message: err.message, stack: err.stack});
  }
  logger.error(msg, err);
  throw err;
}

export default function() {
  logger.setPrefix('[Extractor]');
  return expose(new Extractor);
}

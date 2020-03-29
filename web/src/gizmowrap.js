import settings from './settings.js';
import version from '../version.json';
import Logger from './logger.js';
const logger = Logger.logger.get('[Gizmo]');

export default class Gizmo {

  static init(module) {
    const cfg = {
      print: logger.log.bind(logger),
      printErr: logger.warn.bind(logger),
      locateFile: locateFile,
    }

    return new Promise(resolve => {
      module(cfg).then(gizmo => {
        Gizmo.instance = gizmo;
        if (typeof gizmo.setDebugLevel !== 'undefined') {
          gizmo.setDebugLevel(settings.logLevel || 20);
          gizmo.setLoggerCallback(logCallback);
        }
        resolve();
      });
    });
  }
}

function locateFile(path, prefix, noSuffix) {
  let res = `${settings.url}${prefix || ''}${path}`;
  if (!noSuffix && version.hash) {
    res += `?${version.hash}`;
  }
  return res;
}

function logCallback(log) {
  const text = `${log.module}: ${log.msg}`;
  if (log.level >= 40) {
    logger.error(text);
  } else if (log.level >= 30) {
    logger.warn(text);
  } else {
    logger.log(text);
  }
}

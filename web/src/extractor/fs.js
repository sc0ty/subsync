import Gizmo from '../gizmowrap.js';
import Logger from '../logger.js';
const logger = Logger.logger.get('[Filesystem]');

const EEXIST = 20;
const ENOENT = 44;

export default class Filesystem {

  static isFile(path) {
    const FS = Gizmo.instance.FS;
    try {
      const stat = FS.stat(path);
      return FS.isFile(stat.mode);
    } catch (e) {
      if (e instanceof FS.ErrnoError && e.errno === ENOENT) {
        return false;
      }
      logger.error(`isFile: FS.stat failed for "${path}":`, e);
      throw e;
    }
  }

  static isDir(path) {
    const FS = Gizmo.instance.FS;
    try {
      const stat = FS.stat(path);
      return FS.isDir(stat.mode);
    } catch (e) {
      if (e instanceof FS.ErrnoError && e.errno === ENOENT) {
        return false;
      }
      logger.error(`isDir: FS.stat failed for "${path}":`, e);
      throw e;
    }
  }

  static mkdirIfNotExist(path) {
    if (path.endsWith('/')) {
      path = path.substring(0, path.length-1);
    }
    if (!Filesystem.isDir(path)) {
      Gizmo.instance.FS.mkdir(path);
    }
  }

  static join() {
    return Gizmo.instance.FS.joinPath(arguments);
  }

  static syncfs(populate) {
    return new Promise((resolve, reject) => {
      Gizmo.instance.FS.syncfs(populate, error => {
        error ? reject(error) : resolve();
      });
    });
  }
}

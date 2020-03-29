import JSZip from 'jszip';
import Gizmo from '../gizmowrap.js';
import Filesystem from './fs.js';
import assetList from '../data/assets.json';
import languages from '../data/languages.json';
import Logger from '../logger.js';
const logger = Logger.logger.get('[Assets]');

const ASSETS_DIR = '/assets';

export default class Assets {

  static loadDictionary(langKey, langVal, minWordLen=1) {
    const asset = Assets.getAsset({ type: 'dict', params: [ langKey, langVal ].sort() });
    const reversed = langKey > langVal;
    const dict = new Gizmo.instance.Dictionary();

    const langKeyInfo = languages.find(lang => lang.code3 === langKey);
    const langValInfo = languages.find(lang => lang.code3 === langVal);

    const minKeyLen = langKeyInfo.ngrams || minWordLen;
    const minValLen = langValInfo.ngrams || minWordLen;

    const addEntry = (key, val) => {
      if (key.length >= minKeyLen && val.length >= minValLen) {
        if (langKeyInfo.rightToLeft) key = key.split('').reduce((rev, ch) => ch + rev, '')
        if (langValInfo.rightToLeft) val = val.split('').reduce((rev, ch) => ch + rev, '')
        for (const k of splitNgrams(key, langKeyInfo.ngrams)) {
          for (const v of splitNgrams(val, langValInfo.ngrams)) {
            k && v && dict.add(k.toLowerCase(), v);
          }
        }
      }
    }

    for (const line of asset.split('\n')) {
      if (!line.startsWith('#')) {
        const items = line.split('|');
        const key = items[0];
        for (const val of items.slice(1)) {
          if (reversed) {
            addEntry(val, key);
          } else {
            addEntry(key, val);
          }
        }
      }
    }
    return dict;
  }

  static loadSpeechModel(lang) {
    return JSON.parse(Assets.getAsset({ type: 'speech', params: [ lang ] }));
  }

  static getAsset(asset) {
    const path = Assets.getAssetPath(asset);
    logger.log(`loading asset $(Assets.getAssetName(asset)} from "${path}"`);
    return Gizmo.instance.FS.readFile(path, {encoding: 'utf8'});
  }

  static getAssetName({type, params}) {
    return `${type}/${params.join('-')}`;
  }

  static getAssetPath({type, params}) {
    return Filesystem.join(ASSETS_DIR, type, `${params.join('-')}.${type}`);
  }

  static async preloadAsset(asset) {
    const path = Assets.getAssetPath(asset);
    if (!Filesystem.isFile(path)) {
      const data = Assets.downloadAsset(asset);
      await Assets.extractAsset(data);

      if (asset.type === 'speech') {
        const FS = Gizmo.instance.FS;
        const model = JSON.parse(FS.readFile(path, { encoding: 'utf8' }));
        const sphinx = model.sphinx;
        for (const param in sphinx) {
          if (sphinx[param].startsWith('./')) {
            sphinx[param] = Filesystem.join(ASSETS_DIR, '/speech', sphinx[param]);
          }
        }
        FS.writeFile(path, JSON.stringify(model));
      }
    }
  }

  static async extractAsset(data) {
    const zip = new JSZip();
    await zip.loadAsync(data, { createFolders: true });

    const files = [];
    zip.forEach((path, file) => {
      if (file.dir) {
        Filesystem.mkdirIfNotExist(Filesystem.join(ASSETS_DIR, path));
      } else {
        files.push(file)
      }
    });

    await Promise.all(files.map(async file => {
      const path = Filesystem.join(ASSETS_DIR, file.name);
      const content = await file.async('uint8array');
      Gizmo.instance.FS.writeFile(path, content);
    }));
  }

  static downloadAsset(asset) {
    const description = assetList[Assets.getAssetName(asset)];
    const url = Gizmo.instance.locateFile(description.url, null, true);
    logger.log(`downloading asset ${Assets.getAssetName(asset)} from "${url}"`);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.responseType = 'arraybuffer';
    xhr.send();
    if (!(xhr.status >= 200 && xhr.status < 300 || xhr.status === 304)) {
      throw new Error(`Couldn't download asset from ${url}. Got status ${xhr.status}.`);
    }
    return new Uint8Array(xhr.response);
  }
}

function* splitNgrams(word, size) {
  if (size == null) {
    yield word;
  } else {
    for (let i = 0; i < word.length + 1 - size; i++) {
      yield word.substring(i, i + size);
    }
  }
}

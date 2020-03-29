import i18n from 'es2015-i18n-tag';

export function timeStampFmt(time) {
  const h = Math.floor(time / 3600).toString();
  const m = Math.floor(time / 60 % 60).toString();
  const s = Math.floor(time % 60).toString();
  if (time < 3600)
    return `${m}:${s.padStart(2, '0')}`;
  else
    return `${h}:${m.padStart(2, '0')}:${s.padStart(2, '0')}`;
}

export function timeStampFractionFmt(time) {
  const fraction = Math.floor(time * 1000 % 1000).toString().padStart(3, '0');
  return `${timeStampFmt(time)}:${fraction}`;
}

export function lineFormulaFmt({a, b}) {
  return `${a.toFixed(4)}x${b >= 0 ? '+' : ''}${b.toFixed(3)}`;
}

export function streamTypeName(type) {
  const types = {
    'audio': i18n`audio`,
    'video': i18n`video`,
    'subtitle': i18n`subtitle`,
  };
  const t = type && type.split('/', 1)[0];
  return types[t] || i18n`unknown`;
}

export async function checkSupportedTech() {
  const res = {
    'WebAssembly': typeof WebAssembly !== 'undefined',
    'Web Worker': typeof Worker !== 'undefined',
    'IndexedDB': typeof indexedDB !== 'undefined',
    'ES6 Proxy': typeof Proxy !== 'undefined',
  };
  if (res['Web Worker']) {
    Object.assign(res, await checkSupportedTechInWebWorker());
  }
  return res;
}

function checkSupportedTechInWebWorker() {
  const blob = new Blob([`
    try {
      indexedDB.open('test');
      var hasIndexedDB = true;
    } catch (e) {
      var hasIndexedDB = false;
    }
    postMessage({ 'WebAssembly inside Web Worker': hasIndexedDB });
    `]);
  const url = window.URL.createObjectURL(blob);
  const worker = new Worker(url);
  return new Promise(resolve => {
    worker.onmessage = ev => {
      worker.terminate();
      window.URL.revokeObjectURL(url);
      resolve(ev.data);
    }
    worker.onerror = e => {
      worker.terminate();
      window.URL.revokeObjectURL(url);
      resolve({ 'Web Worker': false });
    }
  });
}

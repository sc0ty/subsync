import Cookies from 'js-cookie';

export class Settings {

  constructor() {
    this.assign(this.defaults);

    let url = [ location.origin ];
    if (typeof baseurl !== 'undefined') {
      url = url.concat(baseurl.split('/'));
    } else {
      const pathname = location.pathname.split('/');
      pathname.pop();
      url = url.concat(pathname);
    }
    this.url = url.filter(x => x !== '' && x !== '.').join('/') + '/';
    this.lang = typeof user_language !== 'undefined' ? user_language : 'en';
  }

  assign(settings) {
    for (const [key, val] of Object.entries(settings)) {
      this[key] = val;
    }
  }

  get defaultJobsNo() {
    if (navigator.hardwareConcurrency && navigator.hardwareConcurrency > 1) {
      return Math.min(navigator.hardwareConcurrency, 6);
    }
    return 2;
  }

  get defaults() {
    return {
      lang: 'pl',
      url: undefined,
      logLevel: 20,
      jobsNo: undefined,
      maxPointDist: 2,
      minPointsNo: 20,
      windowSize: 30 * 60,
      minWordProb: 0.3,
      minWordLen: 5,
      minCorrelation: 0.9999,
      minWordsSim: 0.6,
    }
  }

  get keys() {
    return Object.keys(this.defaults);
  }

  serialize() {
    const res = {}
    for (const key of this.keys) {
      if (key in this) {
        res[key] = this[key];
      }
    }
    return res;
  }

  save() {
    const settings = {};
    const keys = [ 'jobsNo', 'maxPointDist', 'minPointsNo', 'windowSize',
      'minWordProb', 'minWordLen', 'minCorrelation', 'minWordsSim' ];
    for (const key of keys) {
      settings[key] = this[key];
    }
    Cookies.set('settings', settings, { expires: 30 });
  }

  load() {
    const settings = Cookies.getJSON('settings');
    settings && this.assign(settings);
  }
}

export default new Settings();

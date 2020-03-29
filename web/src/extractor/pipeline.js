import Gizmo from '../gizmowrap.js';
import Assets from './assets.js';
import settings from '../settings.js';
import languages from '../data/languages.json';
import Logger from '../logger.js';
const logger = Logger.logger.get('[Pipeline]');

export default class Pipeline {

  constructor(path) {
    this.demux = new Gizmo.instance.Demux(path);
    this.streams = this.demux.getStreamsInfo();
    const lang = getLangFromPath(path);
    if (lang) {
      for (const stream of this.streams) {
        stream.lang = stream.lang || lang;
      }
    }
  }

  makePipeline(stream, params, path) {
    let output = null;
    if (stream.type === 'audio') {
      output = this.makeSpeechPipeline(stream);
    } else if (stream.type === 'subtitle/text') {
      output = this.makeSubPipeline(stream, path);
    }

    const langInfo = stream.lang && languages.find(lang => lang.code3 === stream.lang);
    if (langInfo && langInfo.ngrams) {
      logger.log(`switching to ${langInfo.ngrams}-gram for language ${langInfo.name}`);
      output.setMinWordLen(langInfo.ngrams);
      this.ngramSplitter = new Gizmo.instance.NgramSplitter(langInfo.ngrams);
      output.connectNgramSplitter(this.ngramSplitter);
      output = this.ngramSplitter;
    }

    if (stream.lang && params.otherLang && stream.lang !== params.otherLang) {
      try {
        var dict = Assets.loadDictionary(stream.lang, params.otherLang, settings.minWordLen);
        logger.log(`loaded dict with ${dict.size()} entries`);
        this.translator = new Gizmo.instance.Translator(dict);
        this.translator.setMinWordsSim(settings.minWordsSim);
        output.connectTranslator(this.translator);
        output = this.translator;
      } finally {
        dict && dict.delete();
      }
    }

    return output;
  }

  makeSubPipeline(stream, path) {
    this.dec = new Gizmo.instance.SubtitleDec();
    this.dec.setMinWordLen(settings.minWordLen);
    const enc = stream.enc || this.detectCharEncoding(stream, path);
    if (enc) {
      this.dec.setEncoding(enc);
    }
    const lang = stream.lang && languages.find(lang => lang.code3 === stream.lang);
    if (lang && lang.rightToLeft) {
      logger.log('switching to right-to-left for language', lang.name)
      this.dec.setRightToLeft(true);
    }
    this.demux.connectDec(this.dec, stream.no);
    return this.dec;
  }

  detectCharEncoding(stream, path) {
    if (this.streams.length == 1 && this.streams[0].type === 'subtitle/text') {
      const enc = Gizmo.instance.detectCharEncoding(path, 32*1024*1024);
      logger.log(`detecting character encoding: ${enc}`);
      if (enc === 'ascii') {
        const lang = stream.lang && languages.find(lang => lang.code3 === stream.lang);
        if (lang && lang.enc && lang.enc.length) {
          logger.log(`detected encoding ${lang.enc[0]} for language ${lang.code3}`);
          return lang.enc[0];
        }
      } else if (enc !== 'binary') {
        return enc;
      }
    }
  }

  makeSpeechPipeline(stream) {
    if (!stream.lang) {
      throw {
        message: 'Language not selected',
        file: stream.file && stream.file.name,
      }
    }
    const gizmo = Gizmo.instance;
    const speechModel = Assets.loadSpeechModel(stream.lang);
    logger.log('speech model', speechModel);
    if (!speechModel) {
      throw {
        message: 'Missing speech recognition model',
        file: stream.file && stream.file.name,
        language: stream.lang,
      }
    }

    this.speechRec = new gizmo.SpeechRecognition();
    for (const [key, val] of Object.entries(speechModel.sphinx)) {
      this.speechRec.setParam(key, val);
    }
    this.speechRec.setParam('-mmap', '0');
    this.speechRec.setMinWordProb(settings.minWordProb);
    this.speechRec.setMinWordLen(settings.minWordLen);

    this.dec = new gizmo.AudioDec();
    this.resampler = new gizmo.Resampler();
    this.demux.connectDec(this.dec, stream.no);
    this.dec.connectOutput(this.resampler);

    this.resampler.connectOutput(this.speechRec,
      gizmo.AVSampleFormat[speechModel.sampleformat],
      parseInt(speechModel.samplerate), 32*1024);

    return this.speechRec;
  }

  addSubsListener(listener) {
    this.dec.addSubsListener(listener);
  }

  destroy() {
    if (this.demux) this.demux.delete();
    if (this.dec) this.dec.delete();
    if (this.speechRec) this.speechRec.delete();
    if (this.resampler) this.resampler.delete();
    if (this.ngramSplitter) this.ngramSplitter.delete();
    if (this.translator) this.translator.delete();
    this.demux = undefined;
    this.dec = undefined;
    this.speechRec = undefined;
    this.resampler = undefined;
    this.ngramSplitter = undefined;
    this.translator = undefined;
  }
}

function getLangFromPath(path) {
  const ents = path.split('.');
  const code = ents.length >= 2 && ents[ents.length - 2].match(/[a-zA-Z]{2,3}$/g);
  if (code && code.length) {
    const c = code[0].toLowerCase();
    const lang = languages.find(l => c === l.code3 || c === l.code2 || (l.extraCodes && l.extraCodes.includes(c)));
    return lang && lang.code3;
  }
}

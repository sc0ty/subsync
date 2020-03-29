import { el, place, list } from 'redom';
import i18n from 'es2015-i18n-tag';
import { Overlay } from './overlay.jsx';
import Router from '../router.js';
import Synchronizer from '../synchro.js';
import OptionsPopup from './optionsPopup.jsx';
import settings from '../settings.js';
import { streamTypeName } from '../utils.js';
import assetList from '../data/assets.json';
import languages from '../data/languages.json';
import charEncodings from '../data/charenc.json';
import Logger from '../logger.js';
const logger = Logger.logger.get('[InputScreen]');

export default class InputScreen {

  constructor() {
    <div this='el'>
      <h1>{i18n`Subtitle`}</h1>
      <p>{i18n`Open subtitle file to synchronize.`}</p>
      <InputStream this='sub' id='streams-group-sub' />
      <h1>{i18n`Reference`}</h1>
      <p>{i18n`Open video file to synchronize with. Could be also another subtitle or audio.`}</p>
      <InputStream this='ref' id='streams-group-ref' />
      <div class='buttons'>
        <button this='startBtn' class='highlight' onclick={this.onStartClick.bind(this)}>
          {i18n`Start`}
        </button>
        <button this='optionsBtn' onclick={() => new OptionsPopup().show()}>
          {i18n`Advanced options`}
        </button>
      </div>
    </div>;

    this.sub.types = ['subtitle/text'];
    this.ref.types = ['audio', 'subtitle/text'];
  }

  onStartClick() {
    const sub = this.sub.getParams();
    const ref = this.ref.getParams();
    const errors = validateStreams(sub, ref) || validateAssets(sub, ref);
    if (errors) {
      const errs = errors.map(err => <li>{err}</li>);
      Overlay.showPopup(i18n`Cannot start`, <ul>{errs}</ul>);
    } else {
      Router.update('sync', { sub, ref });
    }
  }
}

class InputStream {
  constructor({id}) {
    const name = `${id}-file`;
    <div this='el'>
      <input this='inputFile' type='file' class='input_file' name={name} onchange={this.onFileOpen.bind(this)} />
      <label this='fileName' for={name} onclick={() => this.inputFile.click()}>{i18n`Select file`}</label>
      {this.streams = place(StreamConfig, {group: id})}
    </div>
  }

  async onFileOpen() {
    if (this.inputFile.files && this.inputFile.files.length) {
      const file = this.inputFile.files[0];
      const spinner = Overlay.showSpinner(i18n`loading file...`);
      try {
        const info = await Synchronizer.instance.getFileInfo(file);
        this.duration = info.duration;
        const streams = Object.values(info.streams).filter(s => this.types.includes(s.type));

        if (streams.length > 0) {
          this.fileName.textContent = file.name;
          this.streams.update(true, {streams});
        } else {
          this.fileName.textContent = i18n`Select file`;
          this.streams.update(false);
          Overlay.showErrorPopup(i18n`Open failed`, {
            message: i18n`There is no matching stream`,
            file: file.name
          });
        }
      } catch (e) {
        logger.warn('Couldn\'t open:', e);
        this.fileName.textContent = i18n`Select file`;
        this.streams.update(false);
        Overlay.showErrorPopup(i18n`Open failed`, e);
      } finally {
        spinner.hide();
      }
    } else {
      this.fileName.textContent = i18n`Select file`;
      this.streams.update(false);
    }
  }

  getParams() {
    if (this.streams.visible && this.inputFile.files.length) {
      const stream = this.streams.view;
      return {
        file: this.inputFile.files[0],
        duration: this.duration,
        no: stream.selectedStream.no,
        type: stream.selectedStream.type,
        lang: stream.lang.value,
        enc: stream.enc.value,
      }
    }
  }
}

class StreamConfig {

  constructor({group}) {
    this.group = group;
    <dl this='el'>
      <dt>{i18n`Select stream:`}</dt>
      <dd>
        {this.streams = list('div', StreamSelector)}
      </dd>
      <dt>{i18n`Select language:`}</dt>
      <dd>
        <select this='lang'>
          <option value=''>{i18n`other`}</option>
          {languages.map(lang => <option value={lang.code3}>{i18n.translate(lang.name)}</option>)}
        </select>
      </dd>
      <dt>{i18n`Character encoding:`}</dt>
      <dd>
        <select this='enc'>
          <option value=''>{i18n`auto detect`}</option>
          {charEncodings.map(e => <option value={e.enc}>{e.enc}: {e.name}</option>)}
        </select>
      </dd>
    </dl>
  }

  update({streams}) {
    this.streams.update(streams, {
      group: this.group,
      select: streams.length ? streams[0].no : null,
      onSelect: this.onStreamSelection.bind(this),
    });
    if (streams.length) {
      this.onStreamSelection(streams[0]);
    }
  }

  onStreamSelection(stream) {
    this.selectedStream = stream;
    this.enc.disabled = stream.type !== 'subtitle/text';
    const lang = languages.find(lang => lang.code3 === stream.lang);
    if (lang) {
      this.lang.value = lang.code3;
    } else {
      this.lang.value = '';
    }
  }
}

class StreamSelector {

  constructor() {
    <label this='el' style={{display: 'block'}}>
      <input this='input' type='radio' />
      <span this='descr' />
    </label>
  }

  update(stream, index, items, {group, onSelect, select}) {
    this.input.name = group;
    this.input.value = stream.no;
    this.input.onchange = ev => onSelect(stream);
    const lang = getLangName(stream.lang.toLowerCase());
    const descr = [ streamTypeName(stream.type), stream.title, lang ];
    this.descr.textContent = `${stream.no+1}: ` + descr.filter(x => x).join(' ');
    if (stream.no === select) {
      this.input.checked = true;
    }
  }
}

function validateStreams(sub, ref) {
  const errors = [];
  if (sub == null || sub.file == null || sub.no == null) {
    errors.push(i18n`subtitle file not set`);
  }
  if (ref == null || ref.file == null || ref.no == null) {
    errors.push(i18n`reference file not set`);
  }
  return errors.length ? errors : null;
}

function validateAssets(sub, ref) {
  const errors = [];
  if (ref && ref.type === 'audio') {
    if (!ref.lang) {
      errors.push(i18n`select reference language`);
    } else if (!(`speech/${ref.lang}` in assetList)) {
      const lang = getLangName(ref.lang);
      errors.push(i18n`synchronization with ${lang} audio is currently not supported`);
    }
  }
  if (sub && sub.lang && ref && ref.lang && sub.lang !== ref.lang) {
    if (!(`dict/${[sub.lang, ref.lang].sort().join('-')}` in assetList)) {
      const subLang = getLangName(sub.lang);
      const refLang = getLangName(ref.lang);
      errors.push(i18n`synchronization between languages ${subLang} - ${refLang} is currently not supported`);
    }
  }
  return errors.length ? errors : null;
}

function getLangName(code3) {
  const lang = languages.find(lang => lang.code3 === code3);
  return lang ? i18n.translate(lang.name) : code3;
}

import { el, list, mount, unmount } from 'redom';
import i18n from 'es2015-i18n-tag';
import { Overlay, OverlayItem } from './overlay.jsx';
import Synchronizer from '../synchro.js';
import Logger from '../logger.js';
const logger = Logger.logger.get('[SaveSubtitlesPopup]');

export default class SaveSubtitlesPopup extends OverlayItem {

  constructor(props) {
    super(i18n`Select format`, true);
    this.props = props;
    <div this='content'>
      {this.formats = list('dl', SaveSubtitleHandler)}
      {props.lang && this.renderAppendLangCheckbox()}
    </div>;
    this.update();
  }

  renderAppendLangCheckbox(update) {
    return(
      <label>
        <input type='checkbox' this='appendLang' onclick={this.update.bind(this)} />
        {i18n`append language code`}
      </label>);
  }

  update() {
    const { fileName, lang } = this.props;
    let baseName = fileName.replace(/\.[^/.]+$/, '');
    if (this.appendLang && this.appendLang.checked && lang) {
      baseName = `${baseName}.${lang}`;
    }
    this.formats.update([
      { fmt: 'srt', name: `${baseName}.srt`, title: 'SubRip' },
      { fmt: 'ass', name: `${baseName}.ass`, title: 'Advanced Substation' },
      { fmt: 'tmp', name: `${baseName}.txt`, title: 'TMP' },
    ], this);
  }
}

class SaveSubtitleHandler {

  constructor() {
    <div this='el'>
      <dt this='title' />
      <dd><a this='button' /></dd>
    </div>;
  }

  update({title, name, fmt}, index, items, parent) {
    this.title.textContent = `${title}:`;
    this.button.textContent = name;
    this.button.onclick = () => {
      parent.hide();
      this.save(fmt, name);
    }
  }

  save(fmt, name) {
    try {
      const subs = Synchronizer.instance.getSynchronizedSubtitles(fmt);
      if (!subs) {
        throw new Error(i18n`Subtitles not ready!`);
      }
      const file = new Blob(subs, {type: 'text/plain'});
      var url = URL.createObjectURL(file);
      var a = <a download={name} href={url} hidden />;
      mount(document.body, a);
      a.click();
    } catch (e) {
      logger.warn('save failed:', e);
      Overlay.showErrorPopup(i18n`Couldn't save subtitles`, e);
    } finally {
      setTimeout(() => {
        unmount(document.body, a);
        window.URL.revokeObjectURL(url);
      }, 0);
    }
  }
}


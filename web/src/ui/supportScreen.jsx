import { el } from 'redom';
import Router from '../router.js';
import { OverlayItem } from './overlay.jsx';
import { simpleList } from './components.jsx';
import { checkSupportedTech } from '../utils.js';
import settings from '../settings.js';

export default class NotSupportedScreen {

  constructor() {
    <div this='el'>
      <h1>{i18n`Browser not supported`}</h1>
      <p>{i18n`SubSync is using solutions that your web browser is not supporting.`}</p>
      <p>{i18n`Choose different browser, or install our`} <a this='desktopLink'>{i18n`SubSync desktop app`}</a>.
      </p>
      <p>{i18n`Popular browsers you could use:`}
        <ul>
          <li><a href='https://www.mozilla.org/pl/firefox/new/' target='_blank'>Mozilla Firefox</a></li>
          <li><a href='https://www.google.com/intl/en/chrome/' target='_blank'>Google Chrome</a></li>
          <li><a href='https://www.chromium.org/getting-involved/download-chromium' target='_blank'>Chromium</a></li>
          <li><a href='https://www.apple.com/safari/' target='_blank'>Safari</a></li>
          <li><a href='https://www.opera.com/' target='_blank'>Opera</a></li>
        </ul>
      </p>
      <p>{i18n`You could ignore this message by clicking "try anyway" but synchronization most likely will fail.`}</p>
      <div class='buttons'>
        <button onclick={this.onDetailsClick.bind(this)} class='highlight'>{i18n`Details`}</button>
        <button onclick={() => Router.update('input')}>{i18n`Try anyway`}</button>
      </div>
    </div>;

    this.desktopLink.target = '_blank';
    this.desktopLink.href = settings.lang + '/download.html';
  }

  async update(props) {
    props = props || {};
    this.supportedTech = props.supportedTech || await checkSupportedTech();
  }

  onDetailsClick() {
    new DetailsPopup(this.supportedTech).show();
  }
}

class DetailsPopup extends OverlayItem {

  constructor(supportedTech) {
    super(i18n`Required technologies`, true);
    this.content = simpleList('ul', 'li', {style: {listStyleType: 'none'}});
    const items = Object.entries(supportedTech).map(this.formatEntry.bind(this));
    this.content.update(items);
  }

  formatEntry([name, supported]) {
    const res = { textContent: `${supported ? '\u2714' : '\u2716'} ${name}` };
    if (!supported) {
      res['class'] = 'error';
    };
    return res;
  }
}

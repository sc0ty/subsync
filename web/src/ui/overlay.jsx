import { el, mount, unmount } from 'redom';
import i18n from 'es2015-i18n-tag';
import settings from '../settings.js';

export class OverlayItem {

  constructor(title, closable) {
    this.title = title;
    this.closable = closable;
  }

  delayedShow(timeout) {
    this.timer = setTimeout(this.show.bind(this), timeout);
    return this;
  }

  show() {
    const containerStyle = {
      display: 'flex',
      position: 'fixed',
      top: 0,
      left: 0,
      minWidth: '100%',
      height: '100%',
      overflow: 'auto',
      zIndex: 1000,
      backgroundColor: 'rgba(0,0,0,0.5)',
    };

    <div this='el' style={containerStyle}>
      <div class='popup'>
        {this.title && this.renderHeader()}
        {this.content}
      </div>
    </div>;

    mount(Overlay.parent, this.el);
    return this;
  }

  renderHeader() {
    return (
      <div style={{display: 'flex', justifyContent: 'space-between'}}>
        {this.title ? <h1>{this.title}</h1> : null}
        {this.closable ? <a class='popup_close' onclick={this.hide.bind(this)}>&times;</a> : null}
      </div>);
  }

  hide() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
    if (this.el) {
      unmount(Overlay.parent, this.el);
      this.el = undefined;
    }
  }
}

export class Overlay {

  static init(parent) {
    this.parent = parent;
  }

  static showSpinner(msg) {
    const spinner = new OverlayItem();
    spinner.content = (
      <p class='spinner'>
        <img src={settings.url + 'img/wait.gif'} />
        {msg || i18n`loading...`}
      </p>);
    return spinner.delayedShow(100);
  }

  static showPopup(title, content) {
    const popup = new OverlayItem(title, true);
    popup.content = content;
    return popup.show();
  }

  static showErrorPopup(title, err) {
    return Overlay.showPopup(title, [
      <p>{getErrorMessage(err)}</p>,
      <pre>{getErrorDetails(err)}</pre>
    ]);
  }
}

function getErrorMessage(e) {
  const msg = e.message || i18n`Error`;
  return msg.charAt(0).toUpperCase() + msg.substring(1);
}

function getErrorDetails(e) {
  if (typeof e === 'object') {
    const fields = [];
    for (const key in e) {
      if (key !== 'message') {
        fields.push(`${key}: ${JSON.stringify(e[key])}`);
      }
    }
    return fields.length ? fields.join('\n') : null;
  } else if (e != null) {
    return JSON.stringify(e, null, 4);
  }
}

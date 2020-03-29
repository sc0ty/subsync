import { el, setAttr, setStyle, list } from 'redom';
import { Overlay } from './overlay.jsx';

export class ProgressBar {

  constructor() {
    this.progressStyle = {width: '0%', height: '100%', overflow: 'hidden'};
    <div this='el' class='progressbar'>
      <div this='progress' style={this.progressStyle}></div>
    </div>;
  }

  set value(val) {
    this.progressStyle.width = (val * 100) + '%';
    setStyle(this.progress, this.progressStyle);
  }
}

export function simpleList(parent, view, props, onUpdate) {
  return list(parent, SimpleListElement, null, {view, props, onUpdate});
}

class SimpleListElement {

  constructor({view, props, onUpdate}) {
    this.el = el(view, props);
  }

  update(attrs) {
    if (typeof attrs === 'string') {
      this.el.textContent = attrs;
    } else {
      setAttr(this.el, attrs);
    }
  }
}

export function infoButton(title, message) {
  return (
    <button class='info' onclick={() => Overlay.showPopup(title, <p>{message}</p>)}>
      {'\u2139'}
    </button>);
}

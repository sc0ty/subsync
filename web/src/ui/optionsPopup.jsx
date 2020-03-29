import { el } from 'redom';
import i18n from 'es2015-i18n-tag';
import { Overlay, OverlayItem } from './overlay.jsx';
import { infoButton } from './components.jsx';
import settings from '../settings.js';
import { version } from '../../version.json';

export default class OptionsPopup extends OverlayItem {

  constructor() {
    super(i18n`Advanced options`, true);
    const descriptions = getDescriptions();

    <div this='content'>
      <dl class='options'>
        <dt>{i18n`Max adjustment`} ({i18n`min`}):</dt>
        <dd>
          <MinNumberOption this='windowSize' min={5} step={1} />
          {infoButton(i18n`Max adjustment`, descriptions.windowSize)}
        </dd>
        <dt>{i18n`Extractor jobs no`}:</dt>
        <dd>
          <NumberOption this='jobsNo' min={1} step={1} />
          {infoButton(i18n`Extractor jobs no`, descriptions.jobsNo)}
        </dd>
        <dt>{i18n`Max points distance`}:</dt>
        <dd>
          <NumberOption this='maxPointDist' min={0} step={0.01} />
          {infoButton(i18n`Max points distance`, descriptions.maxPointDist)}
        </dd>
        <dt>{i18n`Min points no`}:</dt>
        <dd>
          <NumberOption this='minPointsNo' min={0} step={1} />
          {infoButton(i18n`Min points no`, descriptions.minPointsNo)}
        </dd>
        <dt>{i18n`Min word length`}:</dt>
        <dd>
          <NumberOption this='minWordLen' min={0} step={1} />
          {infoButton(i18n`Min word length`, descriptions.minWordLen)}
        </dd>
        <dt>{i18n`Min words similarity`}:</dt>
        <dd>
          <NumberOption this='minWordsSim' min={0} max={1} step={0.01} />
          {infoButton(i18n`Min words similarity`, descriptions.minWordsSim)}
        </dd>
        <dt>{i18n`Min correlation factor`}:</dt>
        <dd>
          <NumberOption this='minCorrelation' min={0} max={1} step={0.00001} />
          {infoButton(i18n`Min correlation factor`, descriptions.minCorrelation)}
        </dd>
        <dt>{i18n`Min speech recognition score`}:</dt>
        <dd>
          <NumberOption this='minWordProb' min={0} max={1} step={0.01} />
          {infoButton(i18n`Min speech recognition score`, descriptions.minWordProb)}
        </dd>
      </dl>
      <p><em>subsync version {version}</em></p>
      <div class='buttons'>
        <button onclick={this.save.bind(this)} class='highlight'>{i18n`OK`}</button>
        <button onclick={this.hide.bind(this)}>{i18n`Cancel`}</button>
        <button onclick={this.init.bind(this, settings.defaults)}>{i18n`Restore defaults`}</button>
      </div>
    </div>;

    this.jobsNo.setDefaultValue(settings.defaultJobsNo);
    this.keys = settings.keys.filter(key => key in this);
    this.init(settings);
  }

  init(settings) {
    for (const key of this.keys) {
      this[key].setValue(settings[key]);
    }
  }

  save() {
    for (const key of this.keys) {
      settings[key] = this[key].getValue();
    }
    settings.save();
    this.hide();
  }
}

class NumberOption {

  constructor(props) {
    this.props = props;
    <input this='el' type='number' />;
  }

  setDefaultValue(defval) {
    this.defval = defval
  }

  setValue(val) {
    if (val == null && this.defval != null) {
      val = this.defval;
    }
    if (this.props.step && this.props.step < 1) {
      const digits = Math.ceil(-Math.log10(this.props.step));
      val = val.toFixed(digits);
    }
    this.el.value = val;
  }

  getValue() {
    let val = this.el.valueAsNumber;
    if (this.props.step && this.props.step >= 1) val = parseInt(val);
    if ('min' in this.props && val < this.props.min) val = this.props.min;
    if ('max' in this.props && val > this.props.max) val = this.props.max;
    return val !== this.defval ? val : this.defval;
  }
}

class MinNumberOption extends NumberOption {

  setValue(val) {
    super.setValue(val / 60);
  }

  getValue() {
    return super.getValue() * 60;
  }
}

function getDescriptions() {
  return {
    windowSize: i18n`Subtitle time will be changed no more than this value. Higher value will result in longer synchronization, but if you set this too low, synchronization will fail.`,
    jobsNo: i18n`Number of concurrent synchronization threads.`,
    maxPointDist: i18n`Maximum acceptable synchronization error, in seconds. Synchronization points with error greater than this will be discarded.`,
    minPointsNo: i18n`Minumum number of synchronization points. Should not be set too high because it could result with generating large number of false positives.`,
    minWordLen: i18n`Minimum word length, in letters. Shorter words will not be used as synchronization points. Applies only to alphabet-based languages.`,
    minWordsSim: i18n`Minimum words similarity for synchronization points. Between 0.0 and 1.0.`,
    minCorrelation: i18n`Minimum correlation factor, between 0.0 and 1.0. Used to determine synchronization result. If correlation factor is smaller than this, synchronization will fail.`,
    minWordProb: i18n`Minimum speech recognition score, between 0.0 and 1.0. Words transcribed with smaller score will be rejected.`,
  }
}

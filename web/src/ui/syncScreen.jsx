import { el, mount, setAttr } from 'redom';
import i18n from 'es2015-i18n-tag';
import SaveSubtitlesPopup from './saveSubsPopup.jsx';
import { ProgressBar, simpleList } from './components.jsx';
import { Overlay } from './overlay.jsx';
import Router from '../router.js';
import Synchronizer from '../synchro.js';
import settings from '../settings.js';
import { timeStampFmt, timeStampFractionFmt, lineFormulaFmt, streamTypeName } from '../utils.js';
import Logger from '../logger.js';
const logger = Logger.logger.get('[SyncScreen]');

export default class SyncScreen {

  constructor() {
    this.subReady = false;
    this.errors = {};
    this.updateTimer = null;
    this.startTime = performance.now();

    <div this='el'>
      <h1>{i18n`Synchronization`}</h1>
      <p>
        <span this='state'>{i18n`Initializing...`}</span>
        <ProgressBar this='progressBar' />
      </p>
      <dl>
        <dt this='errorsTitle' hidden>{i18n`Errors:`}</dt>
        <dd this='errorsBody' hidden>
          { this.errorMsgs = simpleList('ul', 'li', {class: 'error'}) }
          <a onclick={this.showSyncErrors.bind(this)}>{i18n`Show more`}</a>
        </dd>
        <dt>{i18n`Subtitle:`}</dt>
        <dd><span this='subName' /></dd>
        <dt>{i18n`Reference:`}</dt>
        <dd><span this='refName' /></dd>
        <dt>
          <a this='showDetailsBtn' onclick={this.showDetails.bind(this, true)}>
            {i18n`Show details`}
          </a>
          <span this='detailsHeader' hidden>{i18n`Details:`}</span>
        </dt>
        <dd this='detailsBody' hidden>
          <ul>
            <li>{i18n`elapsed`}: <strong this='elapsed'>-</strong></li>
            <li>{i18n`synchronization points`}: <strong this='points'>-</strong></li>
            <li>{i18n`correlation`}: <strong this='correlation'>-</strong></li>
            <li>{i18n`formula`}: <strong this='formula'>-</strong></li>
            <li>{i18n`max change`}: <strong this='maxChange'>-</strong></li>
          </ul>
          <a this='hideDetailsBtn' onclick={this.showDetails.bind(this, false)}>{i18n`hide`}</a>
        </dd>
      </dl>
      <p this='message' />
      <div class='buttons'>
        <button this='stopBtn' disabled>{i18n`Stop`}</button>
        <button this='backBtn' hidden>{i18n`Back`}</button>
        <button this='saveBtn' class='highlight' disabled>{i18n`Save subtitles`}</button>
      </div>
    </div>;

    this.stopBtn.onclick = this.stop.bind(this);
    this.backBtn.onclick = Router.update.bind(Router, 'input');
    this.saveBtn.onclick = () => new SaveSubtitlesPopup(this.out).show();
  }

  update({sub, ref}) {
    this.out = {
      fileName: ref.file.name,
      lang: sub.lang
    };
    this.subName.textContent = this.renderStreamDescription(sub);
    this.refName.textContent = this.renderStreamDescription(ref);
    this.run(sub, ref);
  }

  async run(sub, ref) {
    try {
      var finished = await Synchronizer.instance.run(sub, ref, this);
    } catch (e) {
      logger.error('run:', e);
      Overlay.showErrorPopup(i18n`Synchronization failed`, e);
      var finished = false;
    }
    this.updateStatusDone(Synchronizer.instance.getStatus(), finished);
  }

  stop() {
    Synchronizer.instance.stop();
    this.stopBtn.disabled = true;
    this.setState(i18n`Terminating...`);
  }

  showDetails(show) {
    this.showDetailsBtn.hidden = show;
    this.detailsHeader.hidden = !show;
    this.detailsBody.hidden = !show;
  }

  renderStreamDescription(s) {
    return `${s.file.name}, ${i18n`stream`} ${s.no + 1}: ${streamTypeName(s.type)}`;
  }

  onunmount() {
    clearTimeout(this.updateTimer);
  }

  onSyncStarted() {
    this.setState(i18n`Synchronizing...`);
    this.updateTimer = setInterval(() => this.updateStatus(Synchronizer.instance.getStatus()), 1000);
    this.stopBtn.disabled = false;
  }

  setState(message, mark, sclass) {
    let m = '';
    if (mark === true) {
      m = '\u2714 ';
    } else if (mark === false) {
      m = '\u2716 ';
    }
    this.state.textContent = m + message;
    setAttr(this.state, { class: sclass });
  }

  updateStatus(status, finished) {
    const elapsed = performance.now() - this.startTime;
    this.elapsed.textContent = timeStampFmt(Math.trunc(elapsed / 1000));

    if (status.progress != null) {
      this.progressBar.value = status.progress;
    }

    if (status && status.correlated != null) {
      this.points.textContent = status.points;
      this.correlation.textContent = (status.factor * 100).toFixed(2) + ' %';
      this.formula.textContent = lineFormulaFmt(status.formula);
      this.maxChange.textContent = timeStampFractionFmt(status.maxChange);

      if (status.subReady && !this.subReady) {
        this.subReady = true;
        this.saveBtn.disabled = false;
        this.setState(
          i18n`Got initial synchronization, you could save subtitles already or wait for better result`,
          true, 'sync_success');
      }
    }
  }

  updateStatusDone(status, finished) {
    this.updateStatus(status, finished);
    this.stopBtn.hidden = true;
    this.backBtn.hidden = false;
    clearTimeout(this.updateTimer);

    if (status.subReady) {
      if (status.maxChange && status.maxChange > 0.5) {
        this.setState(i18n`Subtitles synchronized`, true, 'sync_success');
        if (Object.keys(this.errors).length) {
          mount(this.state, <span class='sync_fail'> {i18n`with errors`}</span>);
        }
      } else {
        this.setState(i18n`No need to synchronize`, true, 'sync_success');
      }
      this.saveBtn.disabled = false;
    } else if (finished) {
      if (status.points > settings.minPointsNo / 2
        && status.factor > Math.pow(settings.minCorrelation, 10)
        && status.maxDistance < 2 * settings.maxPointDist) {
        this.setState(i18n`Synchronization inconclusive`);
        this.saveBtn.disabled = false;
      } else {
        this.setState(i18n`Couldn't synchronize`, false, 'sync_fail');
      }
    } else {
      this.setState(i18n`Synchronization terminated`);
    }
  }

  onSyncError(src, err) {
    const msg = syncErrorToString(src, err);
    let group = this.errors[msg];
    if (!group) {
      this.errors[msg] = group = {};
      this.errorMsgs.update(Object.keys(this.errors));
    }
    let fields = group[err.message];
    if (!fields) {
      group[err.message] = fields = {};
    }
    if (typeof err === 'object') {
      for (const key in err) {
        if (key !== 'message') {
          let field = fields[key];
          if (!field) {
            fields[key] = field = new Set();
          }
          field.add(err[key]);
        }
      }
    }

    if (!this.errorsVisible) {
      this.errorsTitle.hidden = false;
      this.errorsBody.hidden = false;
      this.errorsVisible = true;
    }
  }

  showSyncErrors() {
    const content = [];
    for (const [msg, errs] of Object.entries(this.errors)) {
      content.push(<p>{msg}</p>);
      const description = parseErrorsDescription(errs);
      if (description) {
        content.push(<pre>{description}</pre>);
      }
    }
    Overlay.showPopup(i18n`Synchronization errors`, content);
  }
}

function parseErrorsDescription(errors) {
  const details = [];
  for (const [msg, fields] of Object.entries(errors)) {
    details.push(msg);
    for (const key in fields) {
      const vals = Array.from(fields[key]).sort();
      const val = vals.slice(0, 10).join(', ') + (vals.length > 10 ? '...' : '');
      details.push(`${key}: ${val}`);
    }
  }
  return details.join('\n');
}

function syncErrorToString(source, err) {
  const module = typeof err.module === 'string' ? err.module : '';
  if (source === 'sub') {
    if (module.startsWith('SubtitleDec.decode')) {
      return i18n`Some subtitles can't be decoded (invalid encoding?)`;
    } else {
      return i18n`Error during subtitles read`;
    }
  } else if (source === 'ref') {
    if (module.startsWith('SubtitleDec.decode')) {
      return i18n`Some reference subtitles can't be decoded (invalid encoding?)`;
    } else {
      return i18n`Error during reference read`;
    }
  } else {
    return i18n`Unexpected error occurred`;
  }
}

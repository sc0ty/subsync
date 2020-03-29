import Router from './router.js';
import { Overlay } from './ui/overlay.jsx';
import { checkSupportedTech } from './utils.js';
import setTranslation from './translations';
import settings from './settings.js';
import { version } from '../version.json';
import Logger from './logger.js';
const logger = Logger.logger.get();

async function main() {
  settings.load();
  setTranslation(settings.lang);

  const id = 'subsync_app';
  Router.init(document.getElementById('main_content'), id);
  Overlay.init(document.getElementById(id));

  const spinner = Overlay.showSpinner();
  const supportedTech = await checkSupportedTech();
  spinner.hide();

  const missing = Object.entries(supportedTech).filter(x => !x[1]).map(x => x[0]);
  if (missing.length) {
    logger.warn('browser not supported, missing:', missing.join(', '));
    Router.update('notSupported', {supportedTech});
  } else {
    Router.update('input');
  }
}

logger.log(`subsync ${version}`);
document.addEventListener('DOMContentLoaded', main);

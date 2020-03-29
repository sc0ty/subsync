import { i18nConfig }  from 'es2015-i18n-tag';
import pl from './pl.json';

const translations = { pl, en: {} };

export default function setTranslation(lang) {
  console.log(translations)
  i18nConfig({
    locales: lang || 'en',
    translations: translations[lang] || {},
  });
}

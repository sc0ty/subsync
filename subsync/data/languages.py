from collections import namedtuple, ChainMap


LanguageInfo = namedtuple('LanguageInfo', [
    'code3',
    'code2',
    'name',
    'encodings',
    'rightToLeft',
    'ngrams',
    'extraCodes',
])


def mkLanguage(code3=None, code2=None, name=None, encodings=[], rightToLeft=False, ngrams=None, extraCodes=None):
    return LanguageInfo(code3, code2, name, encodings, rightToLeft, ngrams, extraCodes)


languages = [
        mkLanguage( 'alb', 'sq', _('Albanian'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'ara', 'ar', _('Arabic'), ['ISO-8859-6', 'Windows-1256'], rightToLeft=True ),
        mkLanguage( 'bel', 'be', _('Belarusian'), ['ISO-8859-5'] ),
        mkLanguage( 'bul', 'bg', _('Bulgarian'), ['Windows-1251', 'ISO-8859-5'] ),
        mkLanguage( 'cat', 'ca', _('Catalan'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'chi', 'zh', _('Chinese'), ['GB18030'], ngrams=2, extraCodes=[ 'cht', 'chs', 'cmn' ] ),
        mkLanguage( 'cze', 'cs', _('Czech'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'dan', 'da', _('Danish'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'dut', 'nl', _('Dutch'), ['Windows-1252', 'ISO-8859-1'], extraCodes=[ 'nld' ] ),
        mkLanguage( 'eng', 'en', _('English'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'est', 'et', _('Estonian'), ['ISO-8859-15'] ),
        mkLanguage( 'fao', 'fo', _('Faroese'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'fin', 'fi', _('Finnish'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'fre', 'fr', _('French'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'ger', 'de', _('German'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'gla', 'gd', _('Gaelic'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'glg', 'gl', _('Galician'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'gre', 'el', _('Greek'), ['Windows-1253', 'ISO-8859-7'] ),
        mkLanguage( 'heb', 'he', _('Hebrew'), ['Windows-1255', 'ISO-8859-8'], rightToLeft=True ),
        mkLanguage( 'hrv', 'hr', _('Croatian'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'hun', 'hu', _('Hungarian'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'ice', 'is', _('Icelandic'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'ind', 'id', _('Indonesian'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'ita', 'it', _('Italian'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'jpn', 'ja', _('Japanese'), ['CP932', 'ISO-2022-JP-2', 'EUC-JP'], ngrams=3 ),
        mkLanguage( 'kor', 'ko', _('Korean'), ['CP949', 'ISO-2022-KR'], ngrams=2 ),
        mkLanguage( 'lat', 'la', _('Latin'), [] ),
        mkLanguage( 'lav', 'lv', _('Latvian'), ['Windows-1257', 'ISO-8859-13'] ),
        mkLanguage( 'lit', 'lt', _('Lithuanian'), ['Windows-1257', 'ISO-8859-13'] ),
        mkLanguage( 'may', 'ms', _('Malay'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'mlg', 'mg', _('Malagasy'), [] ),
        mkLanguage( 'mlt', 'mt', _('Maltese'), ['ISO-8859-3'] ),
        mkLanguage( 'nor', 'no', _('Norwegian'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'pol', 'pl', _('Polish'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'por', 'pt', _('Portuguese'), ['Windows-1252', 'ISO-8859-1'], extraCodes=[ 'pob' ]),
        mkLanguage( 'rum', 'ro', _('Romanian'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'rus', 'ru', _('Russian'), ['Windows-1251', 'ISO-8859-5', 'KOI8-R'] ),
        mkLanguage( 'slo', 'sk', _('Slovak'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'slv', 'sl', _('Slovenian'), ['Windows-1250', 'ISO-8859-2'] ),
        mkLanguage( 'spa', 'es', _('Spanish'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'srp', 'sr', _('Serbian'), ['Windows-1250', 'ISO-8859-2', 'Windows-1251', 'ISO-8859-5'] ),
        mkLanguage( 'swe', 'sv', _('Swedish'), ['Windows-1252', 'ISO-8859-1'] ),
        mkLanguage( 'tur', 'tr', _('Turkish'), ['Windows-1254', 'ISO-8859-9'] ),
        mkLanguage( 'ukr', 'uk', _('Ukrainian'), ['Windows-1251', 'ISO-8859-5'] ),
]


codes3 = { x.code3: x for x in languages }

codes2 = { x.code2: x for x in languages }

extraCodes = ChainMap(*[ { k: l for k in l.extraCodes } for l in languages if l.extraCodes ])

def get(code=None, code2=None, code3=None, **kwargs):
    if code3 and code3 in codes3:
        return codes3[code3]
    if code2 and code2 in codes2:
        return codes2[code2]
    if code:
        if code in codes3:
            return codes3[code]
        if code in codes2:
            return codes2[code]
        if code in extraCodes:
            return extraCodes[code]
    return mkLanguage(**kwargs)


def getName(code3):
    if code3 in codes3:
        return codes3[code3].name
    return code3

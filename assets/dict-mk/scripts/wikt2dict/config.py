"""
This file contains all configuration necessary for wikt2dict.
Each Wiktionary edition has a configuration class associated with it.
Since Wiktionary editions tend to have similarities, these classes are
subclasses of general configuration classes.
I know that modifying the configuration is more difficult than
in a plain text configuration file, and I do apologize for it,
but it's much easier to use a Python configuration and gives a whole
lot of new features.
"""
from wikt2dict.article_parsers import DefaultArticleParser, LangnamesArticleParser, SectionAndArticleParser
import re
from os import path, makedirs

"""
Here are the default parameters for configuration base classes.
They can be and are overriden in many classes.
"""
base_dir = path.dirname(__file__)
wiktionary_defaults = {
    'wikicodes_file': path.join(base_dir, 'res/wikicodes'),
    'dump_path_base': path.join(base_dir, '../dat/wiktionary'),
    'dump_file_postfix': 'wiktionary.txt',
    'output_file': 'translation_pairs',
    'verbose_output': True,
    'triangle_threshold': 0,
    'triangle_dir': path.join(base_dir, '../dat/triangle'),
    'triangle_verbose': True,
    'only_new_triangles': False,
}

parser_defaults = {
    'blacklist': ['PAGENAME', r'^[\d\-]*$'],  # words that should not appear
    'placeholder': '',
    # allow same language pairs
    # issue with ltwiktionary: multiword articles have t+ templates
    # for the words of the article title
    'allow_synonyms': True,
}

default_parser_defaults = {
    'translation_prefix': r't[\u00f8\+\-]?',
    'wc_field': 1,
    'word_field': 2,
    'features': ['defaultparser'],
}

langname_parser_defaults = {
    'language_name_field': 1,
    'translation_field': 2,
    'translation_entity_delimiter': ',',
    'translation_re': re.compile(r'\[\[([^\[\]]+)\]\]', re.UNICODE),
    'features': ['langnamesparser'],
    'junk_re': None,
}

section_level_parser_defaults = {
    'section_langfield': 1,
    'features': ['sectionlevel'],
}


class DictLikeClass(object):
    """
    All classes inherit this class so that configurations
    can be used as dictionaries.
    """
    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class WiktionaryConfig(DictLikeClass):
    """
    This is the default WiktionaryConfig that each edition's
    configuration class inherits.
    """
    def __init__(self):
        for key, value in wiktionary_defaults.items():
            self[key] = value
        self._parsers = None
        self._parser_configs = None
        self._wikicodes = None

    @property
    def wikicodes(self):
        if not self._wikicodes:
            with open(self.wikicodes_file) as f:
                self._wikicodes = set([l.strip() for l in f])
        return self._wikicodes

    @property
    def dump_url(self):
        return 'http://dumps.wikimedia.org/{0}wiktionary' \
               '/latest/{0}wiktionary-latest-pages-meta-current.xml.bz2'.format(
                   self.wc)

    @property
    def bz2_path(self):
        path_dir = path.join(self.dump_path_base, self.full_name)
        if not path.exists(path_dir):
            makedirs(path_dir)
        return path.join(path_dir, self.wc + '.bz2')

    @property
    def dump_filename(self):
        return self.wc + self.dump_file_postfix

    '''
    @property
    def dump_path(self):
        prefix = path.join(self.dump_path_base, self.full_name)
        if not path.exists(prefix):
            makedirs(prefix)
        return path.join(prefix, self.dump_filename)

    @property
    def output_path(self):
        prefix = path.join(self.dump_path_base, self.full_name)
        if not path.exists(prefix):
            makedirs(prefix)
        return path.join(self.dump_path_base, self.full_name, self.output_file)
    '''

    @property
    def parsers(self):
        """ The parsers need to be initialized exactly once. """
        if not self._parsers:
            self._parsers = list()
            if self._parser_configs:
                for parser_cl, parser_cfg_cl, parser_cfg in self._parser_configs:
                    self._parsers.append((parser_cl, parser_cfg_cl(parser_cfg)))
        return self._parsers


class ParserConfig(DictLikeClass):

    defaults = parser_defaults

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self._skip_trans_re = None
        for key, value in self.defaults.items():
            self[key] = value
        if parser_cfg:
            for key, value in parser_cfg.items():
                self[key] = value
        if wikt_cfg:
            for key, value in wikt_cfg.items():
                self[key] = value

    @property
    def skip_translation_re(self):
        if self._skip_trans_re is None:
            if self.placeholder:
                self.blacklist.append(self.placeholder)
            if self.blacklist:
                self._skip_trans_re = re.compile(
                    r'(' + '|'.join(self.blacklist) + ')',
                    re.UNICODE)
            else:
                self._skip_trans_re = ''
        return self._skip_trans_re

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__.get(key, None)


class DefaultParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(default_parser_defaults)
        self._trad_re = None
        super(DefaultParserConfig, self).__init__(wikt_cfg, parser_cfg)

    @property
    def trad_re(self):
        if not self._trad_re:
            self._trad_re = re.compile(r'\{\{' + self.translation_prefix +
                                       r'\|([^}|]+)\|'  # wikicode
                                       r'([^}|]*)'  # word
                                       r'(?:\|([^}|]*))*\}\}', re.UNICODE)  # rest
        return self._trad_re


class LangnamesParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(langname_parser_defaults)
        self._bracket_re = None
        self._delimiter_re = None
        self._translation_line_re = None
        super(LangnamesParserConfig, self).__init__(wikt_cfg, parser_cfg)

    @property
    def bracket_re(self):
        if not self._bracket_re:
            self._bracket_re = re.compile(r'\([^)]*\)', re.UNICODE)
        return self._bracket_re

    @property
    def delimiter_re(self):
        if not self._delimiter_re:
            self._delimiter_re = re.compile(self.translation_entity_delimiter,
                                            re.UNICODE)
        return self._delimiter_re

    @property
    def translation_line_re(self):
        if not self._translation_line_re:
            self._translation_line_re = re.compile(self.translation_line, re.UNICODE)
        return self._translation_line_re


class SectionLevelParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(section_level_parser_defaults)
        super(SectionLevelParserConfig, self).__init__(wikt_cfg, parser_cfg)


class SectionLevelWiktionaryConfig(WiktionaryConfig):

    def __init__(self):
        self._section_parsers = None
        self._section_parser_configs = None
        super(SectionLevelWiktionaryConfig, self).__init__()

    @property
    def section_parsers(self):
        if not self._section_parsers:
            self._section_parsers = list()
            if self._section_parser_configs:
                for parser_cl, parser_cfg_cl, parser_cfg in self._section_parser_configs:
                    self._section_parsers.append((parser_cl(self, parser_cfg_cl(parser_cfg))))
        return self._section_parsers


class DefaultWiktionaryConfig(WiktionaryConfig):

    def __init__(self):
        super(DefaultWiktionaryConfig, self).__init__()
        try:
            cfg = self.default_cfg
        except AttributeError:
            cfg = {}
        self._parser_configs = [
            [DefaultArticleParser, DefaultParserConfig, cfg]
        ]


class LangnamesWiktionaryConfig(WiktionaryConfig):

    def __init__(self):
        super(LangnamesWiktionaryConfig, self).__init__()
        try:
            cfg = self.langnames_cfg
        except AttributeError:
            cfg = {}
        self._parser_configs = [
            [LangnamesArticleParser, LangnamesParserConfig, cfg]
        ]


class EstonianConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Estonian'
        self.wc = 'et'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/estonian'),
            'translation_line': r'\*\s*([^\s:]+)\s*:(.*)',
        }
        super(EstonianConfig, self).__init__()


class PolishConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Polish'
        self.wc = 'pl'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/polish'),
            'translation_line': r'\*\s*(.*):\s*((\([^\)]*)?\s*(.*))',
            'trim_re': r'<!--.*(?=-->)-->',
            'translation_entity_delimiter': r',\|;',
        }
        super(PolishConfig, self).__init__()


class RussianConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Russian'
        self.wc = 'ru'
        self.langnames_cfg = {
            'langnames': False,
            'translation_line': r'\|([^\=]+)\=\s*(.+)',
            'translation_entity_delimiter': r',\|;',
        }
        super(RussianConfig, self).__init__()


class UkranianConfig(RussianConfig):

    def __init__(self):
        super(UkranianConfig, self).__init__()
        self.full_name = 'Ukrainian'
        self.wc = 'uk'


class SlovenianConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Slovenian'
        self.wc = 'sl'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/slovenian'),
            'translation_line': r'\*\s*([^\s:]+)\s*:(.*)',
            'translation_entity_delimiter': r',\|;',
        }
        super(SlovenianConfig, self).__init__()


class SomaliConfig(SlovenianConfig):

    def __init__(self):
        super(SomaliConfig, self).__init__()
        self.full_name = 'Somali'
        self.wc = 'so'
        self.langnames_cfg = {
            'translation_line': r'\*\s*([^\s:]+)\s*:(.*)',
            'translation_entity_delimiter': r',\|;',
        }


class MalagasyConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Malagasy'
        self.wc = 'mg'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/malagasy'),
            'translation_line': r'\#\s*([^\s:]+)\s*:(.*)',
        }
        super(MalagasyConfig, self).__init__()


class HebrewConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Hebrew'
        self.wc = 'he'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/hebrew'),
            'translation_line': r'{{\u05ea\|([^|}]+)\|([^}]+)}}',
            'translation_re': re.compile(r'([^|]+)', re.UNICODE),
        }
        super(HebrewConfig, self).__init__()


class IdoConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Ido'
        self.wc = 'io'
        self.langnames_cfg = {
            'langnames': False,
            'translation_line': r'\*\s*\{{([^{}]+)}}:\s*([^\n]+)',
            'skip_translation': r'\*:\s*',
        }
        super(IdoConfig, self).__init__()


class ChineseConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Chinese'
        self.wc = 'zh'
        self.langnames_cfg = {
            'langnames': False,
            'translation_line': r'\*\s*\{{([^}]+)}}:\s*(.+)',
        }
        super(ChineseConfig, self).__init__()


class ItalianConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Italian'
        self.wc = 'it'
        self.langnames_cfg = {
            'langnames': False,
            'translation_line': r':\*\{{([^}]+)}}:\s*(.*)',
            'skip_translation_line':
            r'(\<\!\-\-\s*inserisci|inserisci.*traduzioni|altri\ template\ utili)',
            'skip_translation': r'(:\*:|<\!|^\?+$)',
        }
        super(ItalianConfig, self).__init__()


class VietnameseConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Vietnamese'
        self.wc = 'vi'
        self.langnames_cfg = {
            'langnames': False,
            'translation_line': r':\s*\*\s*\{{([^}]+)}}:\s*(.*)',
        }
        super(VietnameseConfig, self).__init__()


class FinnishConfig(LangnamesWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Finnish'
        self.wc = 'fi'
        self.langnames_cfg = {
            'langnames': path.join(base_dir, 'res/langnames/finnish'),
            'translation_line': r'\*\{{0,2}([^}]+)\}{0,2}:\s*(.*)',
        }
        super(FinnishConfig, self).__init__()


class BasqueConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Basque'
        self.wc = 'eu'
        self.default_cfg = {
            'translation_prefix': r'itz',
        }
        super(BasqueConfig, self).__init__()


class BulgarianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Bulgarian'
        self.wc = 'bg'
        self.default_cfg = {
            'translation_prefix': u'\u043f',
        }
        super(BulgarianConfig, self).__init__()


class CatalanConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Catalan'
        self.wc = 'ca'
        self.default_cfg = {
            'translation_prefix': r'trad[\-\+]?',
            'placeholder': r'\?',
        }
        super(CatalanConfig, self).__init__()


class CroatianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Croatian'
        self.wc = 'hr'
        self.default_cfg = {
            'translation_prefix': 'pr',
        }
        super(CroatianConfig, self).__init__()


class CzechConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Czech'
        self.wc = 'cs'
        self.default_cfg = {
            'translation_prefix': r'P',
        }
        super(CzechConfig, self).__init__()


class EnglishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'English'
        self.wc = 'en'
        super(EnglishConfig, self).__init__()


class GermanConfig(SectionLevelWiktionaryConfig):

    def __init__(self):
        super(GermanConfig, self).__init__()
        self.full_name = 'German'
        self.wc = 'de'
        self.allow_synonyms = False
        default_cfg = {
            'trim_re': r'(.*)\#.*(.*)',
            'translation_prefix': r'[\xdc\xfc]',
        }
        self._section_parser_configs = [
            [DefaultArticleParser, DefaultParserConfig, default_cfg]
        ]
        section_cfg = {
            'parsers': [[DefaultArticleParser, DefaultParserConfig, default_cfg]],
            'section_langmap': path.join(base_dir, 'res/langnames/german'),
            'section_re': re.compile(r'==.*\(\{\{[Ss]prache\|(.+)\}\}\)\s*==', re.UNICODE),
        }
        self._parser_configs = [
            [SectionAndArticleParser, SectionLevelParserConfig, section_cfg]
        ]


class LithuanianConfig(SectionLevelWiktionaryConfig):

    def __init__(self):
        super(LithuanianConfig, self).__init__()
        self.full_name = 'Lithuanian'
        self.wc = 'lt'
        self.allow_synonyms = False
        default_cfg = {
            'trim_re': r'(.*)\#.*(.*)',
        }
        self._section_parser_configs = [
            [DefaultArticleParser, DefaultParserConfig, default_cfg]
        ]
        section_cfg = {
            'parsers': [[DefaultArticleParser, DefaultParserConfig, default_cfg]],
            'section_langmap': False,
            'section_re': re.compile(r'^==\s*\{\{(.+)v\}\}\s*==$', re.UNICODE),
        }
        self._parser_configs = [
            [SectionAndArticleParser, SectionLevelParserConfig, section_cfg]
        ]


class EsperantoConfig(WiktionaryConfig):

    def __init__(self):
        super(EsperantoConfig, self).__init__()
        self.full_name = 'Esperanto'
        self.wc = 'eo'
        langnames_cfg = {
            'translation_line': '\*\s*\{{([^}]+)}}:\s*(.+)',
            'langnames': False,
            'junk_re': re.compile(r'(:[^:]*:|\{\{|\}\}|xxx)', re.UNICODE),
        }
        self._parser_configs = [
            [LangnamesArticleParser, LangnamesParserConfig, langnames_cfg],
            [DefaultArticleParser, DefaultParserConfig, {}]
        ]


class FrenchConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'French'
        self.wc = 'fr'
        self.default_cfg = {
            'translation_prefix': r'trad[\-\+]?',
        }
        super(FrenchConfig, self).__init__()


class GalicianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Galician'
        self.wc = 'gl'
        super(GalicianConfig, self).__init__()


class GeorgianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Georgian'
        self.wc = 'ka'
        self.default_cfg = {
            'translation_prefix': u'\u10d7x*',
        }
        super(GeorgianConfig, self).__init__()


class GreekConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Greek'
        self.wc = 'el'
        self.default_cfg = {
            'translation_prefix': u'\u03c4',
            'placeholder': r'[xX\u03c7\u03a7]{3}',
        }
        super(GreekConfig, self).__init__()


class HungarianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Hungarian'
        self.wc = 'hu'
        super(HungarianConfig, self).__init__()


class IcelandicConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Icelandic'
        self.wc = 'is'
        self.default_cfg = {
            'translation_prefix': r'\xfe\xfd\xf0ing',
        }
        super(IcelandicConfig, self).__init__()


class KurdishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Kurdish'
        self.wc = 'ku'
        self.default_cfg = {
            'translation_prefix': r'(?:W\+?|trad)',
        }
        super(KurdishConfig, self).__init__()


class LatinConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Latin'
        self.wc = 'la'
        self.default_cfg = {
            'translation_prefix': r'x',
        }
        super(LatinConfig, self).__init__()


class LimburgishConfig(FrenchConfig):

    def __init__(self):
        super(LimburgishConfig, self).__init__()
        self.full_name = 'Limburgish'
        self.wc = 'li'


class NorwegianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Norwegian'
        self.wc = 'no'
        self.default_cfg = {
            'translation_prefix': r'(?:o|overs|t[\u00f8\+\-]?)',
        }
        super(NorwegianConfig, self).__init__()


class OccitanConfig(FrenchConfig):

    def __init__(self):
        super(OccitanConfig, self).__init__()
        self.full_name = 'Occitan'
        self.wc = 'oc'


class PortugueseConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Portuguese'
        self.wc = 'pt'
        self.default_cfg = {
            'translation_prefix': r'(?:trad[\-\+]?|xlatio)',
        }
        super(PortugueseConfig, self).__init__()


class SerbianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Serbian'
        self.wc = 'sr'
        self.default_cfg = {
            'translation_prefix': u'\u041f',
            'word_field': 3,
            'placeholder': 'XXX',
        }
        super(SerbianConfig, self).__init__()


class SlovakConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Slovak'
        self.wc = 'sk'
        self.default_cfg = {
            'translation_prefix': 'P',
        }
        super(SlovakConfig, self).__init__()


class SpanishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Spanish'
        self.wc = 'es'
        self.default_cfg = {
            'translation_prefix': r'(?:trad|t)[\u00f8\+\-]?',
            'placeholder': r'[\d\?\-\u2013,]',
        }
        super(SpanishConfig, self).__init__()


class SwahiliConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Swahili'
        self.wc = 'sw'
        super(SwahiliConfig, self).__init__()


class SwedishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Swedish'
        self.wc = 'sv'
        self.default_cfg = {
            'translation_prefix': r'\u00f6.?',
        }
        super(SwedishConfig, self).__init__()


class TurkishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Turkish'
        self.wc = 'tr'
        self.default_cfg = {
            'translation_prefix': u'\xe7eviri',
        }
        super(TurkishConfig, self).__init__()


class DanishConfig(SpanishConfig):

    def __init__(self):
        super(DanishConfig, self).__init__()
        self.full_name = 'Danish'
        self.wc = 'da'


class DutchConfig(FrenchConfig):

    def __init__(self):
        super(DutchConfig, self).__init__()
        self.full_name = 'Dutch'
        self.wc = 'nl'


class RomanianConfig(FrenchConfig):

    def __init__(self):
        super(RomanianConfig, self).__init__()
        self.full_name = 'Romanian'
        self.wc = 'ro'


class IndonesianConfig(FrenchConfig):

    def __init__(self):
        super(IndonesianConfig, self).__init__()
        self.full_name = 'Indonesian'
        self.wc = 'id'


class ArabicConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Arabic'
        self.wc = 'ar'
        super().__init__()

class AromanianConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Azeri'
        self.wc = 'az'
        super().__init__()

class PersianConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Persian'
        self.wc = 'fa'
        super().__init__()

class HindiConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Hindi'
        self.wc = 'hi'
        super().__init__()

class JapaneseConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Japanese'
        self.wc = 'ja'
        super().__init__()

class KoreanConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Korean'
        self.wc = 'ko'
        super().__init__()

class MacedonianConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Macedonian'
        self.wc = 'mk'
        super().__init__()

class MalayConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Malay'
        self.wc = 'ms'
        super().__init__()

class ThaiConfig(DefaultWiktionaryConfig):
    def __init__(self):
        self.full_name = 'Thai'
        self.wc = 'th'
        super().__init__()


configs = [
    BasqueConfig(),
    BulgarianConfig(),
    CatalanConfig(),
    ChineseConfig(),
    CzechConfig(),
    CroatianConfig(),
    DanishConfig(),
    DutchConfig(),
    EnglishConfig(),
    EsperantoConfig(),
    EstonianConfig(),
    FinnishConfig(),
    FrenchConfig(),
    GalicianConfig(),
    GermanConfig(),
    GreekConfig(),
    GeorgianConfig(),
    HebrewConfig(),
    HungarianConfig(),
    IcelandicConfig(),
    IdoConfig(),
    ItalianConfig(),
    IndonesianConfig(),
    KurdishConfig(),
    LatinConfig(),
    LithuanianConfig(),
    LimburgishConfig(),
    MalagasyConfig(),
    NorwegianConfig(),
    OccitanConfig(),
    PolishConfig(),
    PortugueseConfig(),
    RomanianConfig(),
    RussianConfig(),
    SerbianConfig(),
    SlovakConfig(),
    SlovenianConfig(),
    SomaliConfig(),
    SpanishConfig(),
    SwahiliConfig(),
    SwedishConfig(),
    TurkishConfig(),
    UkranianConfig(),
    VietnameseConfig(),
    ArabicConfig(),
    AromanianConfig(),
    PersianConfig(),
    HindiConfig(),
    JapaneseConfig(),
    KoreanConfig(),
    MacedonianConfig(),
    MalayConfig(),
    ThaiConfig(),
]


def get_config_by_wc(wc):
    cfgs = [ cfg for cfg in configs if cfg.wc == wc ]
    return cfgs[0]

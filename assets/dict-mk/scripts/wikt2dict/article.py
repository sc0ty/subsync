import re
import logging
from collections import defaultdict

template_re = re.compile(r"\{\{[^\}]*\}\}", re.UNICODE)
default_translation_re = re.compile(
    r"\{\{(t[\u00d8|\-\+])\|([^}]+)\}\}", re.UNICODE)
global_features = ["sourcewc", "article", "has_article"]

# tester method
def uprint(str_):
    print(str_.encode('utf8'))

class ArticleParser(object):
    """ Base class for all article parsers. 
        This class should not be instantiated.
    """

    def __init__(self, wikt_cfg, parser_cfg, filter_langs=None):
        self.cfg = parser_cfg
        self.wikt_cfg = wikt_cfg
        self.pairs = list()
        self.titles = set()
        self.stats = defaultdict(list)
        self.build_skip_re()
        self.build_trim_re()
        if self.cfg['lower'] and self.cfg['lower'] == 1:
            self.lower_all = True
        else:
            self.lower_all = False

    def build_trim_re(self):
        if self.cfg['trim_re']:
            self.trim_re = re.compile(r'' + self.cfg['trim_re'], re.UNICODE)

    def build_skip_re(self):
        if not self.cfg['skip_translation']:
            self.skip_translation_re = None
        else:
            self.skip_translation_re = re.compile(r'' + self.cfg['skip_translation'], re.UNICODE)
        if not self.cfg['skip_translation_line']:
            self.skip_translation_line_re = None
        else:
            self.skip_translation_line_re = re.compile(self.cfg['skip_translation_line'], re.UNICODE)

    def skip_translation_line(self, line):
        if 'PAGENAME' in line:
            return True
        if self.skip_translation_line_re and self.skip_translation_line_re.search(line):
            return True
        return False

    def parse_article(self, article, source_wc=None):
        if self.skip_article(article) == True:
            self.stats["skip_article"].append(article[0])
            return None
        title, text = article
        if self.lower_all:
            text = text.lower()
        self.titles.add(title)
        self.stats["ok"].append(title)
        t = self.get_pairs(text)
        if t:
            self.store_translations(title, t, source_wc)

    def get_pairs(self, text):
        return dict()

    def skip_article(self, article):
        if not article[0] or not article[1]:
            return True
        if not article[1].strip() or not article[0].strip():
            return True
        # ASSUMPTION: articles with a namespace contain no useful data
        if ':' in article[0]:
            return True
        return False

    def store_translations(self, this_word, translations, source_wc=None):
        for wc in translations.keys():
            if len(translations[wc]) > 0:
                self.pairs.extend(
                        [[source_wc, this_word, wc, i, "sourcewc=" + self.wc, \
                      "article=" + this_word] 
                     for i in translations[wc]])

    def write_word_pairs_to_file(self, append=True):
        """ Write output to file
        One pair and its features are written to tab separated file
        """
        fn = self.cfg['dumpdir'] + '/' + self.cfg['fullname'] + '/' + self.cfg[\
                      'word_pairs_outfile']
        if append:
            outf = open(fn, 'a+')
        else:
            outf = open(fn, 'w')
        for p in self.pairs:
            out_str = self.generate_out_str(self.add_features_to_word_pair(p))
            if out_str:
                outf.write(out_str.encode('utf8'))
        outf.close()

    def generate_out_str(self, pair):
        if not pair:
            return None
        if len(pair) < 4:
            return None
        # alphabetic order
        if pair[0] < pair[2]:
            outstr = "\t".join(pair[0:4])
        else:
            outstr = "\t".join(pair[2:4] + pair[0:2])
        feat_d = dict()
        for feat in pair[4:]:
            fields = feat.split('=')
            if not fields[0] in global_features:
                self.log_handler.error('Feature not found {0}'.format(feat))
                continue
            if len(fields) > 1:
                feat_d[fields[0]] = fields[1]
            else:
                feat_d[fields[0]] = '1'
        for feat in global_features:
            if feat in feat_d:
                outstr += "\t" + feat_d[feat]
            else:
                outstr += "\t0"
        outstr += "\n"
        return outstr

    def add_features_to_word_pair(self, pair):
        """ Adding features to translation pairs
        """
        # article of the word exists
        if pair[3] in self.titles:
            pair.append("has_article")
        return pair

    def trim_translation(self, text):
        if self.cfg['trim_re']:
            text = self.trim_re.sub(r'\1\2', text)
        text = text.replace('[', '')
        text = text.replace(']', '')
        text = text.replace('{', '')
        text = text.replace('}', '')
        return text.strip()



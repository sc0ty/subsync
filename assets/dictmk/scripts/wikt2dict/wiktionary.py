class Wiktionary(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.init_parsers()
        self.pairs = list()

    def init_parsers(self):
        self.parsers = list()
        for parser_cl, parser_cfg in self.cfg.parsers:
            self.parsers.append(parser_cl(self.cfg, parser_cfg))

    def parse_articles(self, write_immediately=False):
        with open(self.cfg.output_path, 'w') as self.outf:
            for title, text in self.read_dump():
                pairs = self.extract_translations(title, text)
                if pairs:
                    if write_immediately:
                        self.write_one_article_translations(pairs)
                    else:
                        self.store_translations(pairs)
            if write_immediately is False:
                self.write_all_pairs()

    def extract_translations(self, title, text):
        if self.skip_article(title, text):
            return
        pairs = list()
        for parser in self.parsers:
            for p in parser.extract_translations(title, text):
                if len(p) == 2:
                    pair = ((self.cfg.wc, title, p[0], p[1]), tuple(parser.cfg.features))
                elif len(p) == 4:
                    pair = (p, tuple(parser.cfg.features))
                else:
                    raise Exception('Invalid pair {0}'.format(p))
                pairs.append(pair)
        return set(pairs)

    def skip_article(self, title, text):
        if not title.strip() or not text.strip():
            return True
        if ':' in title:  # skipping namespaced articles
            return True
        return False

    def write_one_article_translations(self, pairs):
        for pair in pairs:
            if self.cfg.verbose_output is True:
                self.outf.write('\t'.join(pair[0]).encode('utf8') + '\n')
            else:
                self.outf.write('\t'.join(pair[0:4]).encode('utf8') + '\n')

    def store_translations(self, pairs):
        for pair, feat in pairs:
            wc1, w1, wc2, w2 = pair[0:4]
            if wc1 < wc2:
                # storing source article too
                self.pairs.append([wc1, w1, wc2, w2, self.cfg.wc, w1] + list(feat))
            else:
                self.pairs.append([wc2, w2, wc1, w1, wc1, w1] + list(feat))

    def write_all_pairs(self):
        for pair in sorted(self.pairs):
            if self.cfg.verbose_output is True:
                self.outf.write('\t'.join(pair) + '\n')
            else:
                self.outf.write('\t'.join(pair[0:4]) + '\n')

    def read_dump(self):
        with open(self.cfg.dump_path, errors='replace') as f:
            title = u''
            article = u''
            page_sep = '%%#PAGE'
            for l in f:
                if l.startswith(page_sep):
                    if title and article:
                        yield title, article
                    title = l.split(page_sep)[-1].strip()
                    article = u''
                else:
                    article += l
            yield title, article

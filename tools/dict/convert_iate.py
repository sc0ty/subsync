#!/usr/bin/env python3

import os
import sys
import xml.parsers.expat
import language_codes_2to3
from dict_tools import Dictionary


banner = '''
# Data extracted from IATE (Interactive Terminology for Europe)
# Download IATE, European Union, 2019.
# https://iate.europa.eu
'''.strip()


class Parser(object):
    def __init__(self, fname):
        self.nodes = []
        self.terms = {}
        self.langs = set()

        self.tid = None
        self.lang = None
        self.term = None
        self.termType = None

        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data

        p.ParseFile(open(fname, 'rb'))

    def start_element(self, name, attrs):
        self.nodes.append(name)

        if name == 'termEntry' and self.nodes == ['martif', 'text', 'body', 'termEntry']:
            assert(attrs['id'].startswith('IATE-'))
            self.tid = int(attrs['id'][5:])

        elif name == 'langSet' and self.nodes == ['martif', 'text', 'body', 'termEntry', 'langSet']:
            lang = attrs['xml:lang']
            self.lang = language_codes_2to3.codes2to3.get(lang, lang)
            if self.lang != 'mul':
                self.langs.add(self.lang)

    def end_element(self, name):
        if self.nodes == ['martif', 'text', 'body', 'termEntry', 'langSet', 'tig']:
            self.collect_term()
            self.term = None
            self.termType = None

        assert(self.nodes[-1] == name)
        self.nodes.pop()

    def char_data(self, data):
        if self.nodes == ['martif', 'text', 'body', 'termEntry', 'langSet', 'tig', 'term']:
            self.term = data

        elif self.nodes == ['martif', 'text', 'body', 'termEntry', 'langSet', 'tig', 'termNote']:
            self.termType = data

    def collect_term(self):
        if self.termType not in ['abbreviation', 'formula'] and self.lang != 'mul' and ' ' not in self.term:
            if self.tid not in self.terms:
                self.terms[self.tid] = {}
            langs = self.terms[self.tid]
            if self.lang not in langs:
                langs[self.lang] = set()
            terms = langs[self.lang]
            terms.add(self.term)


def gen_dict(terms, lang1, lang2, version):
    d = Dictionary(lang1=lang1, lang2=lang2, version=version, banner=banner)
    for term in terms.values():
        if lang1 in term and lang2 in term:
            val = term[lang2]
            for key in term[lang1]:
                d.add(key, val)
    return d


def iter_langs(langs):
    for lang1 in langs:
        for lang2 in langs:
            if lang1 < lang2:
                yield lang1, lang2


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('Use: {} SRC_PATH DST_DIR VERSION [MIN_KEYS]'.format(sys.argv[0]))
        exit(1)

    srcpath = sys.argv[1]
    dstdir  = sys.argv[2]
    version = sys.argv[3]
    minkeys = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    print('Reading file {}'.format(srcpath))
    p = Parser(srcpath)

    for lang1, lang2 in iter_langs(sorted(p.langs)):
        print('')

        try:
            print('Generating dict {}/{}'.format(lang1, lang2))
            d = gen_dict(p.terms, lang1, lang2, version)
            d.validate()

            if len(d) >= minkeys:
                dstpath = os.path.join(dstdir, d.get_name())
                print('Writing dict {}'.format(dstpath, len(d)))
                d.save(dstpath)
            else:
                print('Got only {} keys, SKIPPING'.format(len(d)))

        except Exception as e:
            print('[!] error: ' + str(e))


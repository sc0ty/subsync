#!/usr/bin/env python3

import os
import sys
import xml.parsers.expat
import language_codes_2to3
import dict_tools


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

def gen_dict2(terms, lang1, lang2):
    with open('out/{}-{}.dict'.format(lang1, lang2), 'w') as fp:
        for term in terms.values():
            if lang1 in term and lang2 in term:
                for x in term[lang1]:
                    fp.write('{}|{}\n'.format(x, '|'.join(term[lang2])))

def gen_dict(terms, lang1, lang2):
    d = {}
    for term in terms.values():
        if lang1 in term and lang2 in term:
            val = term[lang2]
            for key in term[lang1]:
                dict_tools.addToDict(d, key, val)
    return d


if __name__ == "__main__":
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)

    fname = sys.argv[1]
    print('reading file {}'.format(fname))
    p = Parser(fname)

    langs = sorted(p.langs)
    for lang1 in langs:
        for lang2 in langs:
            if lang1 < lang2:
                print('generating dict {} / {}'.format(lang1, lang2))
                d = gen_dict(p.terms, lang1, lang2)
                print('  - got {} keys'.format(len(d)))
                if len(d) >= 1000:
                    dict_tools.saveDict(d, '{}/{}-{}.dict'.format(outdir, lang1, lang2))


#!/usr/bin/env python3

import os
import sys
import glob
from language_codes_2to3 import codes2to3
from dict_tools import Dictionary


banner = '''
# Data extracted from Wiktionary https://www.wiktionary.org
'''.strip()


dicts = {}


def get_dict(lang1, lang2, version):
    key = (lang1, lang2)
    if key in dicts:
        return dicts[key]

    try:
        d = Dictionary(lang1=codes2to3[lang1], lang2=codes2to3[lang2], version=version, banner=banner)
        dicts[key] = d
        return d
    except:
        return None


def read_dict(path, no=2):
    print('Reading {}'.format(path))
    with open(path, 'rt', encoding='utf8') as fp:
        for line in fp:
            ent = line.split('\t', no*2+1)
            items = zip(ent[0:no*2:2], ent[1:no*2:2])
            for lang1, val1 in items:
                for lang2, val2 in items:
                    if lang1 != lang2 and ' ' not in val1 and ' ' not in val2:
                        if lang1 > lang2:
                            lang1, lang2 = lang2, lang1
                            val1, val2 = val2, val1

                        d = get_dict(lang1, lang2, version)
                        if d is not None:
                            d.add(val1, val2)


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('Use: {} SRC_DIR DST_DIR VERSION [MIN_KEYS]'.format(sys.argv[0]))
        exit(1)

    srcdir = sys.argv[1]
    dstdir = sys.argv[2]
    version = sys.argv[3]
    minkeys = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    for path in glob.glob(os.path.join(srcdir, '*.2')):
        read_dict(path, 2)

    for path in glob.glob(os.path.join(srcdir, '*.3')):
        read_dict(path, 3)

    codes3to2 = { v: k for v, k in codes2to3.items() }

    while dicts:
        (lang1, lang2), d = dicts.popitem()

        if d.lang1 > d.lang2:
            d = d.transpose()

        d2 = dicts.pop((codes3to2[lang2], codes3to2[lang1]), None)
        if d2:
            if d2.lang2 > d2.lang1:
                d2 = d2.transpose()
            d.merge(d2)

        d.validate()

        if len(d) >= minkeys:
            dstpath = os.path.join(dstdir, d.get_name())
            print('Dict {} writing {}'.format(d.get_name(), dstpath))
            d.save(dstpath)
        else:
            print('Dict {} got only {} keys, SKIPPING'.format(d.get_name(), len(d)))

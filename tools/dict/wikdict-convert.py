#!/usr/bin/env python3

import os
import sys
import glob
from language_codes_2to3 import codes2to3
from sqlite2dict import *


banner = '''
# Data extracted from Wiktionary [1] by the DBnary project [2].
# Converted to SQLite database for WikDikt online translator [3]
# and thanks to courtesy of Karl Bartel [4] used in here.
#
# 1. https://www.wiktionary.org
# 2. http://kaiko.getalp.org/about-dbnary
# 3. http://www.wikdict.com/page/contact
# 4. http://www.karl.berlin
'''.strip()


def list_dicts(path):
    res = {}
    for srcname in glob.glob(os.path.join(path, '*-*.sqlite3')):
        name = os.path.basename(srcname).split('.', 1)[0]
        langs = name.split('-', 1)
        lang1 = codes2to3[langs[0]]
        lang2 = codes2to3[langs[1]]
        res[(lang1, lang2)] = srcname
    return res


def read_sql_dict(path, transpose=False):
    d = readDictFromSqliteDB(path)
    validateDict(d)
    if transpose:
        return transponseDict(d)
    else:
        return d


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Use: {} [SRC-DIR] [DST-DIR] [VERSION]'.format(sys.argv[0]))
        exit(1)

    srcdir = sys.argv[1]
    dstdir = sys.argv[2]
    version = sys.argv[3]

    os.makedirs(dstdir, exist_ok=True)

    srcs = list_dicts(srcdir)
    while srcs:
        d1 = {}
        d2 = {}

        (lang1, lang2), path = srcs.popitem()
        transpose = lang1 > lang2

        try:
            print('Reading dict {}/{} from {}'.format(lang1, lang2, path))
            d1 = read_sql_dict(path, transpose)
        except Exception as e:
            print('[!] error: ' + str(e))

        path = srcs.get((lang2, lang1), None)
        if path:
            try:
                print('Reading dict {}/{} from {}'.format(lang2, lang1, path))
                d2 = read_sql_dict(path, not transpose)
            except Exception as e:
                print('[!] error: ' + str(e))

        d = mergeDicts(d1, d2)
        if transpose:
            lang1, lang2 = lang2, lang1

        if len(d) >= 10000:
            dstpath = os.path.join(dstdir, '{}-{}.dict'.format(lang1, lang2))
            print('Writing dict {}, keys: {}'.format(dstpath, len(d)))

            try:
                saveDict(d, dstpath, banner=banner, langs=(lang1, lang2), version=version)
            except Exception as e:
                print('[!] error: ' + str(e))

        else:
            print('Got only {} keys, SKIPPING'.format(len(d)))

        print('')


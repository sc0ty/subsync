#!/usr/bin/env python3

import os
import sys
import glob
from language_codes_2to3 import codes2to3
from sqlite2dict import readDictFromSqliteDB
from dict_tools import Dictionary


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


def read_sql_dict(d, path, transpose=False):
    readDictFromSqliteDB(d, path)
    d.validate()
    if transpose:
        return d.transponse()
    else:
        return d


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Use: {} SRC_DIR DST_DIR VERSION [MIN_KEYS]'.format(sys.argv[0]))
        exit(1)

    srcdir = sys.argv[1]
    dstdir = sys.argv[2]
    version = sys.argv[3]
    minkeys = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    srcs = list_dicts(srcdir)
    while srcs:
        (lang1, lang2), path = srcs.popitem()
        d = Dictionary(lang1=lang1, lang2=lang2, version=version, banner=banner)

        try:
            print('Reading dict {}/{} from {}'.format(lang1, lang2, path))
            read_sql_dict(d, path)
            if lang1 > lang2:
                d = d.transpose()
        except Exception as e:
            print('[!] error: ' + str(e))

        path = srcs.get((lang2, lang1), None)
        if path:
            try:
                d2 = Dictionary(lang1=lang2, lang2=lang1, version=version, banner=banner)
                print('Reading dict {}/{} from {}'.format(lang2, lang1, path))
                read_sql_dict(d2, path)
                if lang2 > lang1:
                    d2 = d2.transpose()
                d.merge(d2)
            except Exception as e:
                print('[!] error: ' + str(e))

        if len(d) >= minkeys:
            dstpath = os.path.join(dstdir, d.get_name())
            print('Writing dict {}'.format(dstpath))

            try:
                d.save(dstpath)
            except Exception as e:
                print('[!] error: ' + str(e))

        else:
            print('Got only {} keys, SKIPPING'.format(len(d)))

        print('')


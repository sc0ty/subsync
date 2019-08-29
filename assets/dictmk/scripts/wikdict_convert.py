#!/usr/bin/env python3

import os
import sys
import glob
import sqlite3
from language_codes_2to3 import codes2to3
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


def dict_add(d, key, val):
    if ' ' in key:
        for k in key.split():
            k = k.strip()
            if len(k) >= 5:
                dict_add(d, k, val)
    elif ' ' in val:
        vals = [ v.strip() for v in val.split() if len(v.strip()) >= 5 ]
        dict_add(d, key, vals)
    else:
        d.add(key, val)


def read_sql_dict(d, path, transpose=False):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute('select written_rep, trans_list from translation')
    for row in cursor:
        key = row[0].strip()
        vals = row[1].split('|')
        for val in vals:
            dict_add(d, key, val.strip())

    d.validate()
    if transpose:
        return d.transponse()
    else:
        return d


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('wikdict_convert: Use: {} SRC_DIR DST_DIR VERSION [MIN_KEYS]'.format(sys.argv[0]))
        exit(1)

    srcdir = sys.argv[1]
    dstdir = sys.argv[2]
    version = sys.argv[3]
    minkeys = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    srcs = list_dicts(srcdir)
    while srcs:
        (lang1, lang2), path = srcs.popitem()
        d = Dictionary(lang1=lang1, lang2=lang2, version=version, banner=banner)

        print('wikdict_convert: Reading {}'.format(path))
        read_sql_dict(d, path)
        if lang1 > lang2:
            d = d.transpose()

        path = srcs.get((lang2, lang1), None)
        if path:
            d2 = Dictionary(lang1=lang2, lang2=lang1, version=version, banner=banner)
            print('wikdict_convert: Reading {}'.format(path))
            read_sql_dict(d2, path)
            if lang2 > lang1:
                d2 = d2.transpose()
            d.merge(d2)

        if len(d) >= minkeys:
            dstpath = os.path.join(dstdir, d.get_name())
            print('wikdict_convert: Dict {} writing {}'.format(d.get_name(), dstpath))
            d.save(dstpath)

        else:
            print('wikdict_convert: Dict {} got only {} keys, SKIPPING'.format(d.get_name(), len(d)))


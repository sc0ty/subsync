#!/usr/bin/env python3

import sys
import os
import glob
import csv
from sqlite2dict import *


if __name__ == "__main__":
    codes = {}

    os.makedirs('dict', exist_ok=True)

    with open('language-codes-3b2.csv', 'rt') as file:
        reader = csv.reader(file)
        for row in reader:
            codes[row[1]] = row[0]

    for srcname in glob.glob('wikdict/*-*.sqlite3'):
        name = os.path.basename(srcname).split('.', 1)[0]
        langs = name.split('-', 1)

        try:
            dstname = 'dict/' + codes[langs[0]] + '-' + codes[langs[1]] + '.dict'

            print(srcname + ' => ' + dstname)
            d = readDictFromSqliteDB(srcname)
            validateDict(d)
            if len(d) > 0:
                saveDict(d, dstname)
            else:
                print('empty dict, skipping')
        except Exception as e:
            print('error: ' + str(e))
        print('')


#!/usr/bin/env python3

import os
import sys
import glob
from dict_tools import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('use: {} [version]'.format(sys.argv[0]))

    os.makedirs('res', exist_ok=True)
    version = sys.argv[1]
    dicts = set()

    for fname in glob.glob('dict/*-*.dict'):
        langs = os.path.basename(fname).split('.', 1)[0].split('-', 1)
        dicts.add(tuple(sorted(langs)))

    banner = ''
    if os.path.isfile('banner.txt'):
        with open('banner.txt', 'rt') as fp:
            banner = fp.read()

    for lang1, lang2 in dicts:
        path1 = 'dict/{}-{}.dict'.format(lang1, lang2)
        path2 = 'dict/{}-{}.dict'.format(lang2, lang1)

        d = {}
        if os.path.isfile(path1):
            print(path1, end='')
            d = loadDict(path1)
        else:
            print('-' * len(path1), end='')

        if os.path.isfile(path2):
            print(' + ' + path2, end='')
            d2 = loadDict(path2)
            d2 = transponseDict(d2)
            d = mergeDicts(d, d2)
        else:
            print(' + ' + '-' * len(path2), end='')

        dstpath = 'res/{}-{}.dict'.format(lang1, lang2)
        print(' => {} ({})'.format(dstpath, len(d)), end='')

        if len(d) >= 1000:
            print('')
            b = '#dictionary/{}/{}/{}\n{}'.format(lang1, lang2, version, banner)
            saveDict(d, dstpath, b)

        else:
            print('\tSKIPPING')


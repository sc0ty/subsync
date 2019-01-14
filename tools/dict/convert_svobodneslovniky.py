#!/usr/bin/env python3

import sys
import os
from dict_tools import Dictionary


banner = '''
# Data extracted from Free English-Czech Dictionary https://www.svobodneslovniky.cz
# Copyright (c)  2016–2019  xHire <xhire@svobodneslovniky.cz>.
# Licence: GNU/FDL 1.1
'''.strip()


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('Use: {} SRC_FILE DST_DIR VERSION'.format(sys.argv[0]))
        exit(1)

    srcpath = sys.argv[1]
    dstdir  = sys.argv[2]
    version = sys.argv[3]
    minkeys = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    print('Reading dict {}'.format(srcpath))

    d = Dictionary(lang1='cze', lang2='eng', version=version, banner=banner)

    with open(srcpath, 'rt', encoding='utf8') as fp:
        for line in fp:
            if line and line[0] != '#':
                ent = line.split('\t')
                if len(ent) >= 2:
                    val = ent[0]
                    key = ent[1]

                    if key and val and ' ' not in key and ' ' not in val:
                        d.add(key, val)

    d.validate()

    if len(d) >= minkeys:
        dstpath = os.path.join(dstdir, d.get_name())
        print('Writing dict {}'.format(dstpath))
        d.save(dstpath)
    else:
        print('Got only {} keys, SKIPPING'.format(len(d)))

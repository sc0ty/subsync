#!/usr/bin/env python3

import sys
import os
from dict_tools import *


banner = '''
# Data extracted from Free English-Czech Dictionary https://www.svobodneslovniky.cz
# Copyright (c)  2016–2019  xHire <xhire@svobodneslovniky.cz>.
# Licence: GNU/FDL 1.1
'''.strip()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Use: {} SRC_FILE DST_DIR VERSION'.format(sys.argv[0]))
        exit(1)

    srcpath = sys.argv[1]
    dstdir  = sys.argv[2]
    version = sys.argv[3]

    print('Reading dict {}'.format(srcpath))

    d = {}
    with open(srcpath, 'rt') as fp:
        for line in fp:
            if line and line[0] != '#':
                ent = line.split('\t')
                if len(ent) >= 2:
                    key = ent[0]
                    val = ent[1]

                    if key and val and ' ' not in key and ' ' not in val:
                        addToDict(d, key, val)

    validateDict(d)
    dstpath = os.path.join(dstdir, 'cze-eng.dict')
    print('Writing dict {}, keys: {}'.format(dstpath, len(d)))

    saveDict(d, dstpath, banner=banner, langs=('cze', 'eng'), version=version)

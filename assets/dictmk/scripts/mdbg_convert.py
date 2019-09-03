#!/usr/bin/env python3

import sys
import os
import re
from dict_tools import Dictionary


banner = '''
# Data extracted from CC-CEDICT https://www.mdbg.net
# License: Creative Commons Attribution-ShareAlike 4.0 International License
'''.strip()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('mdbg_convert: Use: {} SRC_FILE DST_DIR VERSION'.format(sys.argv[0]))
        exit(1)

    srcpath = sys.argv[1]
    dstdir  = sys.argv[2]
    version = sys.argv[3]

    print('mdbg_convert: Reading {}'.format(srcpath))

    chi_eng = Dictionary(lang1='chi', lang2='eng', version=version, banner=banner)
    cht_eng = Dictionary(lang1='cht', lang2='eng', version=version, banner=banner)
    chs_eng = Dictionary(lang1='chs', lang2='eng', version=version, banner=banner)
    chs_cht = Dictionary(lang1='chs', lang2='cht', version=version, banner=banner)
    dicts = [ chi_eng, cht_eng, chs_eng, chs_cht ]

    strip_re = re.compile(r'\[.*?\]|\(.*?\)')

    def addEntry(cht=None, chs=None, eng=None):
        if chs and cht:
            chs_cht.add(chs, cht)
        if chs and eng:
            chs_eng.add(chs, eng)
            chi_eng.add(chs, eng)
        if cht and eng:
            cht_eng.add(chs, eng)
            chi_eng.add(chs, eng)

    with open(srcpath, 'rt', encoding='utf8') as fp:
        for line in fp:
            if line and line[0] != '#':
                try:
                    trad, simp, rest = line.split(' ', 2)
                    keys = set([trad, simp])
                    vals = rest[rest.index(']')+1:].split('/')

                    for val in vals:
                        eng = strip_re.sub('', val).strip()
                        if ' ' in eng:
                            for e in eng.split():
                                e = e.strip()
                                if len(e) >= 5:
                                    addEntry(trad, simp, e)
                        else:
                            addEntry(trad, simp, eng)

                    '''
                    for key in keys:
                        for val in vals:
                            val = strip_re.sub('', val).strip()

                            if key and val and ' ' not in key and ' ' not in val:
                                chi_eng.add(key, val)
                                '''
                except e as Exception:
                    print('mdbg_convert: error:', e)

    for d in dicts:
        d.validate()
        dstpath = os.path.join(dstdir, d.get_name())
        print('mdbg_convert: Dict {} writing {}'.format(d.get_name(), dstpath))
        d.save(dstpath)

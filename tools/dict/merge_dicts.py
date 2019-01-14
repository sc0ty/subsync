#!/usr/bin/env python3

import os
import sys
import glob
from dict_tools import Dictionary


multi_banner = '''
# Dictionary data acquired from multiple sources:
'''.strip()

def make_dict(dst, srcs, minkeys=1):
    dicts = []
    for src in srcs:
        print('Reading {}'.format(src))
        d = Dictionary(src)
        dicts.append(d)

    dicts = sorted(dicts, reverse=True, key=lambda d: len(d))

    banners = []
    for d in dicts:
        if d.banner and not d.banner in banners:
            banners.append(d.banner)

    res = dicts[0]
    for d in dicts[1:]:
        res.merge(d)
        res.banner += '\n' + d.banner

    if len(banners) == 1:
        res.banner = banners[0]
    elif len(banners) > 1:
        banners.insert(0, multi_banner)
        res.banner = '\n\n'.join(banners)

    res.version = version_to_str(max([ parse_version(d.version) for d in dicts ]))
    res.validate()

    if len(res) >= minkeys:
        print('Generating dict {}'.format(dst))
        res.save(dst)
    else:
        print('Got only {} keys, SKIPPING'.format(len(res)))

    print('')


def find_dicts(name, dirs):
    paths = [ os.path.join(d, name) for d in dirs ]
    return  [ p for p in paths if os.path.isfile(p) ]


def parse_version(version, default=[0, 0, 0]):
    try:
        return [ int(x) for x in version.split('.') ]
    except:
        return default


def version_to_str(version):
    return '.'.join([ str(x) for x in version ])


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('Use: {} SRC_DIR1 [SRC_DIR2] [SRC_DIR3...] DST_DIR MIN_KEYS'.format(sys.argv[0]))
        exit(1)

    srcdirs = sys.argv[1:-2]
    dstdir  = sys.argv[-2]
    minkeys = int(sys.argv[-1])

    os.makedirs(dstdir, exist_ok=True)

    processed = set()

    for srcdir in srcdirs:
        for srcname in glob.glob(os.path.join(srcdir, '???-???.dict')):
            name = os.path.basename(srcname)
            if name not in processed:
                processed.add(name)
                srcpaths = find_dicts(name, srcdirs)
                dstpath = os.path.join(dstdir, name)
                make_dict(dstpath, srcpaths, minkeys)


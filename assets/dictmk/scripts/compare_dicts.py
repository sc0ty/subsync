#!/usr/bin/env python3

import os
import sys
import glob
from dict_tools import Dictionary


def load_dicts(dirpath):
    dicts = {}
    paths = glob.glob(os.path.join(dirpath, '???-???.dict'))
    i = 0
    for path in paths:
        i += 1
        pr = 100.0 * i / len(paths)
        print('\rprocessing {}: {:.0f}%'.format(dirpath, pr), end='', file=sys.stderr)
        sys.stdout.flush()

        name = os.path.basename(path)
        dicts[name] = Dictionary(path).items_count()

    print('\r{}\r'.format(' ' * (len(dirpath) + 18)), end='', file=sys.stderr)
    sys.stdout.flush()
    return dicts


def sort_cnts(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('compare_dicts: Use: {} OLD_DICTS_DIR NEW_DICTS_DIR'.format(sys.argv[0]))
        exit(1)

    olddir = sys.argv[1]
    newdir = sys.argv[2]

    old = load_dicts(olddir)
    new = load_dicts(newdir)

    diffs = {}
    removed = old.keys() - new.keys()
    added = new.keys() - old.keys()

    for key in sorted(old):
        if key in new:
            diffs[key] = new[key] - old[key]
        else:
            removed.append(key)

    for key, val in sort_cnts({k: -old[k] for k in removed}):
        print('{}: {:+d} REMOVED'.format(key, val))

    for key, val in sort_cnts({k: new[k] for k in added}):
        print('{}: {:+d} ADDED'.format(key, val))

    for key, val in sort_cnts(diffs):
        print('{}: {:+d}'.format(key, val))


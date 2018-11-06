#!/usr/bin/env python

import sys
import re


def mkPattern(*args):
    pattern = '|'.join([ '^{}$\\s'.format(x.replace(' ', '\\s')) for x in args ])
    return re.compile(pattern)


if len(sys.argv) < 2:
    print('usage: {} [FILE]'.format(sys.argv[0]))
    sys.exit(1)


excludeRe = mkPattern(
        'import gettext',
        '_ = gettext.gettext')

for fname in sys.argv[1:]:
    lines = []

    with open(fname, 'r') as fp:
        for line in fp:
            if not excludeRe.match(line):
                lines.append(line)

    with open(fname, 'w') as fp:
        for line in lines:
            fp.write(line)


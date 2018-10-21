#!/usr/bin/env python3
import sys
import subprocess
import re


DEFAULT_FNAME = 'version.py'

def update_version(fname = DEFAULT_FNAME):
    try:
        version_long = subprocess.check_output(['git', 'describe', '--tags']).decode('UTF-8').strip()
        v = version_long[re.search('\d', version_long).start():].split('-')
        if len(v) > 1:
            version = '{}.{}'.format(v[0], v[1])
        else:
            version = '{}.0'.format(v[0])
    except Exception as e:
        print('Version not recognized, using default, reason: ' + str(e))
        version_long = 'custom'
        version = '0.0.0'

    print('version number: {} ({})'.format(version, version_long))

    with open(fname, 'w') as fp:
        fp.write('version = "{}"\n'.format(version_long))
        fp.write('version_short = "{}"\n'.format(version))

    return version


if __name__ == "__main__":
    fname = DEFAULT_FNAME
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    update_version(fname)


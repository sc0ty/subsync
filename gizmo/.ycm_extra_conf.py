# based on https://github.com/Valloric/ycmd/blob/master/.ycm_extra_conf.py

import ycm_core
import os


basePath = os.path.dirname(os.path.abspath(__file__))


def getFlags():
    flags = [ '-x', 'c++' ]
    try:
        with open(os.path.join(basePath, 'ycm.flags'), 'rt') as fp:
            flags += fp.read().split()
    except:
        flags += [
                '-Wall',
                '-Wextra',
                '-pedantic',
                '-std=c++11',
                '-I.',
                ]
    return flags


def FlagsForFile(filename, **kwargs):
    return {
            'flags': getFlags(),
            'include_paths_relative_to_dir': basePath,
            'do_cache': True
            }


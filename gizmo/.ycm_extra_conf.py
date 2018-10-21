import ycm_core

def FlagsForFile(filename):
    try:
        from ycm_flags import flags
    except:
        flags = [ '-x', 'c++', '-Wall', '-Wextra', '-std=c++11', '-I.' ]

    return {
        'flags': flags,
        'do_cache': True
    }

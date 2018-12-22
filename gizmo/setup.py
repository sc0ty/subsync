from setuptools import setup, Extension
import setuptools.command.build_ext
import setuptools
import os
import sys
import sysconfig
import re
import subprocess
from collections import OrderedDict
import tempfile


def get_arg(name):
    for i, arg in enumerate(sys.argv):
        if arg.startswith(name + '='):
            val = arg.split('=', 1)[1]
            del sys.argv[i]
            return val


def get_paths(base_dir, *suffixes):
    if base_dir:
        res = [ os.path.join(base_dir, p) for p in suffixes ]
        return [ p for p in res if os.path.isdir(p) ]
    else:
        return []


_has_pkg_config = None
def has_pkg_config():
    global _has_pkg_config

    if _has_pkg_config != None:
        return _has_pkg_config

    try:
        cmd = ['pkg-config', '--version']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        proc.wait()
        _has_pkg_config = True
    except FileNotFoundError:
        _has_pkg_config = False
        print('there is no pkg-config')

    return _has_pkg_config


def get_pkg_config(method, *modules):
    cmd = ['pkg-config', method, *modules]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        status = proc.wait()
        if status:
            print(' '.join(cmd))
            print('FAILED with status {}'.format(status))
            print(err.decode('utf8'))
            exit(1)

        return out.decode('utf8').split()
    except Exception as e:
        print(' '.join(cmd))
        print('FAILED: {}'.format(str(e)))
        exit(1)


def strip_prefixes(items, *prefixes):
    def strip_item(item):
        for prefix in prefixes:
            if item.startswith(prefix):
                return item[len(prefix):]

    res = [ strip_item(item) for item in items ]
    return [ item for item in res if item ]


def has_flag(compiler, flagname):
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def get_version():
    try:
        version_long = subprocess.check_output(['git', 'describe', '--tags']).decode('UTF-8').strip()
        v = version_long[re.search('\d', version_long).start():].split('-')
        if len(v) > 1:
            return '{}.{}'.format(v[0], v[1])
        else:
            return '{}.0'.format(v[0])
    except Exception as e:
        print('Version not recognized, using default, reason: ' + str(e))
        return '0.0.0'


bit64 = sys.maxsize > 2**32

sources = [
        'extractor.cpp',
        'correlator.cpp',
        'media/demux.cpp',
        'media/stream.cpp',
        'media/audiodec.cpp',
        'media/resampler.cpp',
        'media/subdec.cpp',
        'media/speechrec.cpp',
        'text/translator.cpp',
        'text/dictionary.cpp',
        'text/utf8.cpp',
        'text/wordsqueue.cpp',
        'math/point.cpp',
        'math/line.cpp',
        'math/linefinder.cpp',
        'general/exception.cpp',
        'general/logger.cpp',
        'general/thread.cpp',
        'python/wrapper.cpp',
        'python/general.cpp',
        'python/extractor.cpp',
        'python/media.cpp',
        'python/stream.cpp',
        'python/correlator.cpp',
        'python/translator.cpp',
        ]

ffmpeg_libs = [
        'avdevice',
        'avformat',
        'avfilter',
        'avcodec',
        'swresample',
        'swscale',
        'avutil',
        ]

sphinx_libs = [
        'pocketsphinx',
        'sphinxbase',
        ]

use_pkg_config = get_arg('--use-pkg-config') or os.environ.get('USE_PKG_CONFIG')
if use_pkg_config == None:
    use_pkg_config = has_pkg_config()

ffmpeg_dir       = get_arg('--ffmpeg-dir')       or os.environ.get('FFMPEG_DIR')
sphinxbase_dir   = get_arg('--sphinxbase-dir')   or os.environ.get('SPHINXBASE_DIR')
pocketsphinx_dir = get_arg('--pocketsphinx-dir') or os.environ.get('POCKETSPHINX_DIR')

libraries = []

include_dirs = []
include_dirs += '.'
include_dirs += get_paths(ffmpeg_dir,       '', 'include')
include_dirs += get_paths(sphinxbase_dir,   '', 'include')
include_dirs += get_paths(pocketsphinx_dir, '', 'include')

library_dirs = []
library_dirs += [ sysconfig.get_path('include') ]
library_dirs += get_paths(ffmpeg_dir,       '', 'lib')
library_dirs += get_paths(sphinxbase_dir,   '', 'lib')
library_dirs += get_paths(pocketsphinx_dir, '', 'lib')

global_cflags  = []
global_ldflags = []

if use_pkg_config and use_pkg_config != 'no' and has_pkg_config():
    pkgs = [ 'lib' + name for name in ffmpeg_libs ] + sphinx_libs

    include_dirs   += strip_prefixes(get_pkg_config('--cflags-only-I', *pkgs), '-I')
    library_dirs   += strip_prefixes(get_pkg_config('--libs-only-L', *pkgs),   '-L', '-R')
    libraries      += strip_prefixes(get_pkg_config('--libs-only-l', *pkgs),   '-l')

    global_cflags  += get_pkg_config('--cflags-only-other', *pkgs)
    global_ldflags += get_pkg_config('--libs-only-other',   *pkgs)

else:
    libraries += ffmpeg_libs + sphinx_libs

if sys.platform == 'win32':
    arch = 'x64' if bit64 else 'win32'
    include_dirs += get_paths(sphinxbase_dir,   os.path.join('include', 'win32'))
    library_dirs += get_paths(sphinxbase_dir,   os.path.join('bin', 'Release', arch))
    library_dirs += get_paths(pocketsphinx_dir, os.path.join('bin', 'Release', arch))


try:
    import pybind11
    pybind11_path = pybind11.get_include()
    include_dirs += [ pybind11_path ]

    # workaround for snapcraft putting this elsewhere
    include_dirs += [ pybind11_path.replace('{0}usr{0}'.format(os.path.sep), os.path.sep, 1) ]
except ImportError:
    print('cannot import pybind11')


ext_modules = [
        Extension(
            'gizmo',
            sources = sources,
            include_dirs = include_dirs,
            library_dirs = library_dirs,
            libraries = libraries,
            define_macros = [ ('NDEBUG', '1') ],
            language = 'c++',
            ),
        ]


class build_ext(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        cflags  = global_cflags
        ldflags = global_ldflags

        if self.compiler.compiler_type in ['unix', 'cygwin', 'mingw32']:
            self.setup_unix(cflags, ldflags)

        elif self.compiler.compiler_type == 'msvc':
            self.setup_msvc(cflags, ldflags)

        for ext in self.extensions:
            ext.extra_compile_args = cflags
            ext.extra_link_args = ldflags

        super().build_extensions()

    def setup_unix(self, cflags, ldflags):
        cflags += [ '-O3', '-g' ]

        if sys.platform == 'darwin':
            cflags += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

        if has_flag(self.compiler, '-std=c++14'):
            cflags.append('-std=c++14')
        else:
            cflags.append('-std=c++11')

        optional_flags = [
                '-fvisibility=hidden',
                '-fomit-frame-pointer',
                '-fexpensive-optimizations',
                ]

        cflags += [ fl for fl in optional_flags if has_flag(self.compiler, fl) ]

    def setup_msvc(self, cflags, ldflags):
        cflags += [ '/EHsc' ]


setup(
    name = 'gizmo',
    version = get_version(),
    author = 'Michał Szymaniak',
    author_email = 'sc0typl@gmail.com',
    url = 'https://github.com/sc0ty/subsync',
    description = 'SubSync gizmo library',
    long_description = '',
    ext_modules = ext_modules,
    setup_requires = ['pybind11>=2.2'],
    cmdclass = {'build_ext': build_ext},
    zip_safe = False,
)

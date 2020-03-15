import sys, os, glob, re, subprocess, shutil
import distutils.cmd, distutils.command.build_py
import setuptools
import setuptools.command.build_ext
from setuptools import setup, Extension
import sysconfig, subprocess, tempfile


class build_py(distutils.command.build_py.build_py):
    def run(self):
        try:
            config_path = os.path.join('subsync', 'config.py')
            config_path_template = os.path.join('subsync', 'config.py.template')

            if not os.path.isfile(config_path):
                print('copying {} -> {}'.format(config_path_template, config_path))
                shutil.copyfile(config_path_template, config_path)
        except:
            pass

        update_version = False
        try:
            version_long, version = read_version()
            update_version = version_long is not None

            import subsync
            update_version = subsync.version()[1] != version_long
        except:
            pass

        if update_version:
            write_version_file(version_long, version)

        super().run()


class build_ext(setuptools.command.build_ext.build_ext):
    user_options = setuptools.command.build_ext.build_ext.user_options + [
            ('use-pkg-config=', None, 'yes/no, use pkg-config to obtain information about installed libraries'),
            ('ffmpeg-dir=', None, 'ffmpeg library location'),
            ('sphinxbase-dir=', None, 'sphinxbase library location'),
            ('pocketsphinx-dir=', None, 'pocketsphinx library location'),
            ]

    def initialize_options(self):
        super().initialize_options()
        self.cflags  = []
        self.ldflags = []
        self.use_pkg_config   = os.environ.get('USE_PKG_CONFIG')
        self.ffmpeg_dir       = os.environ.get('FFMPEG_DIR')
        self.sphinxbase_dir   = os.environ.get('SPHINXBASE_DIR')
        self.pocketsphinx_dir = os.environ.get('POCKETSPHINX_DIR')

    def finalize_options(self):
        super().finalize_options()

        use_pkg_config = False
        if self.use_pkg_config is None:
            use_pkg_config = self.has_pkg_config()
        elif self.use_pkg_config == 'yes':
            use_pkg_config = True
            if not self.has_pkg_config():
                raise Exception('pkg-config not available')
        elif self.use_pkg_config == 'no':
            use_pkg_config = False
        else:
            raise Exception('--use-pkg-config invalid value {}, should be yes or no'.format(self.use_pkg_config))

        if self.ffmpeg_dir is not None and not os.path.isdir(self.ffmpeg_dir):
            raise Exception('ffmpeg directory does not exists: '.format(self.ffmpeg_dir))
        if self.sphinxbase_dir is not None and not os.path.isdir(self.sphinxbase_dir):
            raise Exception('sphinxbase directory does not exists: '.format(self.sphinxbase_dir))
        if self.pocketsphinx_dir is not None and not os.path.isdir(self.pocketsphinx_dir):
            raise Exception('pocketsphinx directory does not exists: '.format(self.pocketsphinx_dir))

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

        if use_pkg_config:
            pkgs = [ 'lib' + name for name in ffmpeg_libs ] + sphinx_libs
            self.cflags       += self.get_pkg_config('--cflags-only-other', pkgs)
            self.ldflags      += self.get_pkg_config('--libs-only-other',   pkgs)
            self.include_dirs += self.get_pkg_config('--cflags-only-I', pkgs, strip_prefixes=['-I'])
            self.library_dirs += self.get_pkg_config('--libs-only-L', pkgs, strip_prefixes=['-L', '-R'])
            self.libraries    += self.get_pkg_config('--libs-only-l', pkgs, strip_prefixes=['-l'])

        else:
            self.libraries += ffmpeg_libs + sphinx_libs

        import pybind11
        self.include_dirs += self.get_paths(pybind11.get_include(), '')
        self.include_dirs += self.get_paths(pybind11.get_include(True), '')

        self.include_dirs += self.get_paths(self.ffmpeg_dir,       '', 'include')
        self.include_dirs += self.get_paths(self.sphinxbase_dir,   '', 'include')
        self.include_dirs += self.get_paths(self.pocketsphinx_dir, '', 'include')

        self.library_dirs += [ sysconfig.get_path('include') ]
        self.library_dirs += self.get_paths(self.ffmpeg_dir,       '', 'lib')
        self.library_dirs += self.get_paths(self.sphinxbase_dir,   '', 'lib')
        self.library_dirs += self.get_paths(self.pocketsphinx_dir, '', 'lib')

        if sys.platform == 'win32':
            bit64 = sys.maxsize > 2**32
            arch = 'x64' if bit64 else 'win32'
            self.include_dirs += self.get_paths(self.sphinxbase_dir,   os.path.join('include', 'win32'))
            self.library_dirs += self.get_paths(self.sphinxbase_dir,   os.path.join('bin', 'Release', arch))
            self.library_dirs += self.get_paths(self.pocketsphinx_dir, os.path.join('bin', 'Release', arch))

    def build_extensions(self):
        if self.compiler.compiler_type in ['unix', 'cygwin', 'mingw32']:
            self.setup_unix()

        elif self.compiler.compiler_type == 'msvc':
            self.setup_msvc()

        super().build_extensions()

    def setup_unix(self):
        self.cflags += [ '-O3', '-g' ]

        if sys.platform == 'darwin':
            self.cflags += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

        if self.has_flag('-std=c++14'):
            self.cflags += ['-std=c++14']
        else:
            self.cflags += ['-std=c++11']

        optional_flags = [
                '-fvisibility=hidden',
                '-fomit-frame-pointer',
                '-fexpensive-optimizations',
                ]

        self.cflags += [ fl for fl in optional_flags if self.has_flag(fl) ]

        for ext in self.extensions:
            ext.extra_compile_args = self.cflags
            ext.extra_link_args    = self.ldflags

    def setup_msvc(self):
        self.cflags += [ '/EHsc' ]

    def get_paths(self, base_dir, *suffixes):
        if base_dir:
            res = [ os.path.realpath(os.path.join(base_dir, p)) for p in suffixes ]
            return [ p for p in res if os.path.isdir(p) ]
        else:
            return []

    def has_pkg_config(self):
        try:
            cmd = ['pkg-config', '--version']
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate()
            proc.wait()
            return True
        except FileNotFoundError:
            return False

    def get_pkg_config(self, method, modules, strip_prefixes=[]):
        cmd = ['pkg-config', method] + modules
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            status = proc.wait()
            if status:
                print(' '.join(cmd))
                print('FAILED with status {}'.format(status))
                print(err.decode('utf8'))
                exit(1)

            res = []
            for param in out.decode('utf8').split():
                for prefix in strip_prefixes:
                    if param.startswith(prefix):
                        param = param[ len(prefix): ]
                res.append(param)
            return res

        except Exception as e:
            print(' '.join(cmd))
            print('FAILED: {}'.format(str(e)))
            exit(1)

    def has_flag(self, flagname):
        with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
            f.write('int main (int argc, char **argv) { return 0; }')
            try:
                self.compiler.compile([f.name], extra_postargs=[flagname])
            except setuptools.distutils.errors.CompileError:
                return False
        return True


class gen_gui(distutils.cmd.Command):
    description = 'Generate GUI files'
    user_options = [
            ('wxformbuilder=', None, 'path to wxFormBuilder binary'),
            ]

    def initialize_options(self):
        self.wxformbuilder = 'wxformbuilder'

    def finalize_options(self):
        pass

    def run(self):
        files = glob.glob(os.path.join('subsync', 'gui', 'layout', '*.fbp'))
        excludeRe = self._mk_pattern('import gettext', '_ = gettext.gettext')

        for src in files:
            subprocess.check_call([self.wxformbuilder, '-g', src])

            dst = src[0:-4] + '.py'
            lines = []

            with open(dst, 'r') as fp:
                for line in fp:
                    if not excludeRe.match(line):
                        lines.append(line)

            with open(dst, 'w') as fp:
                for line in lines:
                    fp.write(line)

    def _mk_pattern(self, *args):
        pattern = '|'.join([ '^{}$\\s'.format(x.replace(' ', '\\s')) for x in args ])
        return re.compile(pattern)


class gen_locales(distutils.cmd.Command):
    description = 'Generate locales file'
    user_options = [
            ('xgettext=', None, 'path to xgettext binary'),
            ('out=', None, 'path to output messages file'),
            ]

    def initialize_options(self):
        self.xgettext = 'xgettext'
        self.out_path = os.path.join('subsync', 'messages.po')

    def finalize_options(self):
        pass

    def run(self):
        files = glob.glob(os.path.join('subsync', '**', '*.py'), recursive=True)
        cmd = [self.xgettext, '--language=Python', '-o', self.out_path] + sorted(files)
        subprocess.check_call(cmd)


class gen_version(distutils.cmd.Command):
    description = 'Generate version file'
    user_options = [
            ('out=', None, 'path to version file')
            ]

    def initialize_options(self):
        self.out_path = None

    def finalize_options(self):
        pass

    def run(self):
        version_long, version = read_version()
        write_version_file(version_long, version, self.out_path)


def read_version():
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

    return version_long, version


def write_version_file(version_long, version, path=None):
    if path is None:
        path = os.path.join('subsync', 'version.py')

    print('writing version number {} -> {}'.format(version_long, path))
    with open(path, 'w') as fp:
        fp.write('version = "{}"\n'.format(version_long))
        fp.write('version_short = "{}"\n'.format(version))


setup(
        name = 'subsync',
        version = read_version()[1],
        author = 'Michał Szymaniak',
        author_email = 'sc0typl@gmail.com',
        url = 'https://github.com/sc0ty/subsync',
        description = 'Subtitle Speech Synchronizer',
        license='GPLv3',
        python_requires = '>=3.5',
        packages = [
            'subsync',
            'subsync.synchro',
            'subsync.assets',
            'subsync.data',
            'subsync.gui',
            'subsync.gui.layout',
            'subsync.gui.components',
            'subsync.gui.components.batchlist',
            'gizmo'
            ],
        entry_points = {'gui_scripts': ['subsync=subsync.__main__:subsync']},
        setup_requires = [
            'pybind11>=2.4',
            ],
        install_requires = [
            'aiohttp>=2.3',
            'certifi',
            'pysubs2>=0.2.4',
            'pycryptodome>=3.9;platform_system=="Linux"',
            'cryptography>=2.8;platform_system!="Linux"',
            'PyYAML',
            'pybind11>=2.4',
            ],
        extras_require = {
            'GUI': [ 'wxPython>=4.0' ],
            },
        scripts = ['bin/subsync'],
        cmdclass = {
            'build_py': build_py,
            'build_ext': build_ext,
            'gen_gui': gen_gui,
            'gen_locales': gen_locales,
            'gen_version': gen_version,
            },
        package_data = {
            'subsync': [
                'key.pub',
                os.path.join('img', '*.png'),
                os.path.join('img', '*.ico'),
                os.path.join('locale', '*', 'LC_MESSAGES', '*.mo'),
                ],
            },
        ext_modules = [
            Extension('gizmo',
                sources = [
                    'gizmo/extractor.cpp',
                    'gizmo/correlator.cpp',
                    'gizmo/synchro/synchronizer.cpp',
                    'gizmo/media/demux.cpp',
                    'gizmo/media/stream.cpp',
                    'gizmo/media/audiodec.cpp',
                    'gizmo/media/resampler.cpp',
                    'gizmo/media/subdec.cpp',
                    'gizmo/media/speechrec.cpp',
                    'gizmo/text/translator.cpp',
                    'gizmo/text/dictionary.cpp',
                    'gizmo/text/words.cpp',
                    'gizmo/text/ssa.cpp',
                    'gizmo/text/ngrams.cpp',
                    'gizmo/text/utf8.cpp',
                    'gizmo/text/wordsqueue.cpp',
                    'gizmo/math/point.cpp',
                    'gizmo/math/line.cpp',
                    'gizmo/math/linefinder.cpp',
                    'gizmo/general/exception.cpp',
                    'gizmo/general/logger.cpp',
                    'gizmo/general/platform.cpp',
                    'gizmo/python/wrapper.cpp',
                    'gizmo/python/general.cpp',
                    'gizmo/python/extractor.cpp',
                    'gizmo/python/media.cpp',
                    'gizmo/python/stream.cpp',
                    'gizmo/python/correlator.cpp',
                    'gizmo/python/translator.cpp',
                    ],
                include_dirs = [ 'gizmo' ],
                define_macros = [
                    ('NDEBUG', '1'),
                    ('USE_PYBIND11', '1'),
                    ],
                language = 'c++',
                ),
            ]
        )

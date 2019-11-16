import sys, os, glob, re, subprocess, shutil
import distutils.cmd
import distutils.command.build_py
from setuptools import setup


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

        try:
            update_version = False
            version_long, version = read_version()
            update_version = version_long is not None

            import subsync
            update_version = subsync.version()[1] != version_long

        finally:
            if update_version:
                write_version_file(version_long, version)

        super().run()


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
        cmd = [self.xgettext, '--language=Python', '-o', self.out_path, *sorted(files)]
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
        packages = [
            'subsync',
            'subsync.synchro',
            'subsync.assets',
            'subsync.data',
            'subsync.gui',
            'subsync.gui.layout',
            'subsync.gui.components',
            'subsync.gui.components.batchlist',
            ],
        entry_points = {'gui_scripts': ['subsync=subsync.__main__:subsync']},
        install_requires = [
            'aiohttp>=2.3',
            'certifi',
            'pysubs2>=0.2.4',
            'pycryptodome>=3.9',
            'PyYAML',
            'wxPython>=4.0',
            ],
        scripts = ['bin/subsync'],
        cmdclass = {
            'build_py': build_py,
            'gen_gui': gen_gui,
            'gen_locales': gen_locales,
            'gen_version': gen_version,
            },
        package_data={
            'subsync': [
                'key.pub',
                os.path.join('img', '*.png'),
                os.path.join('img', '*.ico'),
                os.path.join('locale', '*', 'LC_MESSAGES', '*.mo'),
                ],
            },
        )

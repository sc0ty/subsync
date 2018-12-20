import sys
import os
import glob
import re
import subprocess
import distutils.cmd


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
        files = glob.glob(os.path.join('subsync', 'gui', '*.fbp'))
        excludeRe = self._mk_pattern('import gettext', '_ = gettext.gettext')

        for src in files:
            subprocess.check_call([self.wxformbuilder, '-g', src])

            dst = src[0:-4] + '_layout.py'
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


def update_version(fname=os.path.join('subsync', 'version.py')):
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


version = update_version()

desc = dict(
        name = 'subsync',
        description = 'Subtitle Speech Synchronizer',
        version = version,
        )


if sys.platform == 'win32':
    from cx_Freeze import setup, Executable

    build_exe = {
        'packages': ['idna', 'asyncio'],
        'excludes': ['updatelangs', 'tkinter', 'tcl', 'ttk'],
        'include_files': [
            os.path.join('subsync', 'img'),
            os.path.join('subsync', 'locale'),
            os.path.join('subsync', 'key.pub'),
            *glob.glob('*.dll'),
            ],
        'include_msvcr': True,
    }

    bdist_msi = {
        'upgrade_code': '{30cde9a7-1f56-49ef-8701-4d6bf8dee50a}',
        'data': {
            'Shortcut': [
                ('StartMenuShortcut',        # Shortcut
                 'StartMenuFolder',          # Directory
                 'Subtitle Speech Synchronizer', # Name
                 'TARGETDIR',              # Component
                 '[TARGETDIR]subsync.exe', # Target
                 None,                     # Arguments
                 None,                     # Description
                 None,                     # Hotkey
                 None,                     # Icon
                 None,                     # IconIndex
                 None,                     # ShowCmd
                 'TARGETDIR'               # WkDir
                 ),
            ],
        },
    }

    executables = [
        Executable(
            os.path.join('subsync', '__main__.py'),
            base = 'Win32GUI',
            targetName = 'subsync.exe',
            icon = os.path.join('subsync', 'img', 'icon.ico'),
        )
    ]

    setup(**desc,
            options = {
                'build_exe': build_exe,
                'bdist_msi': bdist_msi,
                },
            cmdclass = {
                'gen_gui': gen_gui,
                'gen_locales': gen_locales,
                },
            executables = executables,
            )

else:
    from setuptools import setup

    setup(**desc,
            packages=['subsync', 'subsync.assets', 'subsync.data', 'subsync.gui'],
            entry_points={'gui_scripts': ['subsync=subsync.__main__:subsync']},
            install_requires=['aiohttp', 'pysubs2', 'pycryptodome'],
            cmdclass = {
                'gen_gui': gen_gui,
                'gen_locales': gen_locales,
                },
            package_data={
                'subsync': [
                    'key.pub',
                    os.path.join('img', '*.png'),
                    os.path.join('img', '*.ico'),
                    os.path.join('locale', '*', 'LC_MESSAGES', '*.mo'),
                    ],
                },
            data_files = [
                ('share/icons/hicolor/scalable/apps', ['resources/subsync.svg']),
                ('share/applications', ['resources/subsync.desktop']),
                ],
            )

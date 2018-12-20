import sys
import os
import glob
import subprocess
import version


desc = dict(
        name = 'subsync',
        description = 'Subtitle Speech Synchronizer',
        version = version.version_short,
        )


if sys.platform == 'win32':
    from cx_Freeze import setup, Executable

    dlls = glob.glob(os.path.join(os.path.realpath('..'), '*.dll'))
    build_exe = {
        'packages': ['idna', 'asyncio'],
        'excludes': ['updatelangs', 'tkinter', 'tcl', 'ttk'],
        'include_files': ['img', 'locale', 'key.pub'] + dlls,
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
            '__main__.py',
            base = 'Win32GUI',
            targetName = 'subsync.exe',
            icon = os.path.join('img', 'icon.ico'),
        )
    ]

    setup(**desc,
        options = {
            'build_exe': build_exe,
            'bdist_msi': bdist_msi,
        },
        executables = executables,
    )

else:
    from setuptools import setup

    setup(**desc,
            entry_points={'gui_scripts': ['subsync=__main__:subsync']},
            packages=['assets', 'data', 'gui'],
    )

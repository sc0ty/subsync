from cx_Freeze import setup, Executable
import sys
import os
import glob
import subprocess
import version


build_exe = {
    'packages': ['idna'],
    'excludes': ['updatelangs', 'tkinter', 'tcl', 'ttk'],
    'include_files': ['img', 'key.pub'],
}

if sys.platform == 'win32':
    build_exe['include_files'] += glob.glob(os.path.join(os.path.realpath('..'), '*.dll'))
    build_exe['include_msvcr'] = True

    target_base = 'Win32GUI'
    target_suffix = '.exe'

else:
    target_base = None
    target_suffix = ''

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
        base = 'Console',
        targetName = 'subsync-dbg' + target_suffix,
        icon = os.path.join('img', 'icon.ico'),
    ),
    Executable(
        '__main__.py',
        base = target_base,
        targetName = 'subsync' + target_suffix,
        icon = os.path.join('img', 'icon.ico'),
    )
]

setup(
    name = 'subsync',
    description = 'Subtitle Speech Synchronizer',
    version = version.version_short,
    options = {
        'build_exe': build_exe,
        'bdist_msi': bdist_msi,
    },
    executables = executables,
)

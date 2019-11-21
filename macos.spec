# -*- mode: python ; coding: utf-8 -*-

try:
    exec(open((SPECPATH or '.') + '/subsync/version.py').read())
    info_plist = { 'CFBundleShortVersionString': version_short }
except:
    info_plist = None


a = Analysis(['bin/subsync'],
        pathex=['.'],
        binaries=[],
        datas=[
            ('LICENSE', '.'),
            ('subsync/key.pub', '.'),
            ('subsync/img', 'img'),
            ('subsync/locale', 'locale'),
            ],
        hiddenimports=['certifi'],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=None,
        noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='subsync',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False )

coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='subsync')

app = BUNDLE(coll,
        name='subsync.app',
        icon='resources/icon.icns',
        bundle_identifier='subsync',
        info_plist=info_plist)

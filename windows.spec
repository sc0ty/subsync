# -*- mode: python ; coding: utf-8 -*-


main_a = Analysis(['bin/subsync'],
        pathex=['.'],
        binaries=[],
        datas=[
            ('LICENSE', '.'),
            ('subsync/key.pub', '.'),
            ('subsync/img', 'img'),
            ('subsync/locale', 'locale'),
            ],
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=None,
        noarchive=False)

main_pyz = PYZ(main_a.pure, main_a.zipped_data, cipher=None)

main_exe = EXE(main_pyz,
        main_a.scripts,
        [],
        exclude_binaries=True,
        name='subsync',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon='resources/icon.ico')

main_dbg = EXE(main_pyz,
        main_a.scripts,
        [],
        exclude_binaries=True,
        name='subsync-debug',
        debug=True,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        icon='resources/icon.ico')

main_coll = COLLECT(main_exe,
        main_dbg,
        main_a.binaries,
        main_a.zipfiles,
        main_a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='subsync')

portable_a = Analysis(['bin/portable'],
        pathex=['.'],
        binaries=[],
        datas=[
            ('LICENSE', '.'),
            ('subsync/key.pub', '.'),
            ('subsync/img', 'img'),
            ('subsync/locale', 'locale'),
            ],
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=None,
        noarchive=False)

portable_pyz = PYZ(portable_a.pure, portable_a.zipped_data, cipher=None)

portable_exe = EXE(portable_pyz,
        portable_a.scripts,
        portable_a.binaries,
        portable_a.zipfiles,
        portable_a.datas,
        [],
        name='subsync-portable',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        icon='resources/icon.ico')

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ('LICENSE', '.'),
                 ('README.md', '.'),
                 ('subsync/key.pub', 'subsync'),
                 ('subsync/img', 'subsync/img'),
                 ('subsync/locale', 'subsync/locale'),
                 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='subsync',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources/icon.ico')

dbg = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='subsync-debug',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='resources/icon.ico')

coll = COLLECT(exe,
               dbg,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='subsync')

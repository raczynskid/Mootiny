# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['D:\\Python\\rts'],
             binaries=[],
             datas=[('assets/fonts/AmaticSC-Regular.ttf','assets/fonts'),('assets/sprites/barn.png','assets/sprites'),('assets/sprites/cow_static.png','assets/sprites'),('assets/sprites/interface.png','assets/sprites'),('assets/sprites/barn_open.png','assets/sprites')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='__main__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

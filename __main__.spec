# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['D:\\Python\\rts'],
             binaries=[],
             datas=[('assets/misc/cows_icon.ico','assets/misc'),('assets/fonts/AmaticSC-Regular.ttf','assets/fonts'),('assets/sprites/cows_cloud.png','assets/sprites'),('assets/sprites/cows_grass.png','assets/sprites'),('assets/sprites/cows_grass2.png','assets/sprites'),('assets/sprites/cows_grass_flower1.png','assets/sprites'),('assets/sprites/barn.png','assets/sprites'),('assets/sprites/cow_static.png','assets/sprites'),('assets/sprites/interface.png','assets/sprites'),('assets/sprites/barn_open.png','assets/sprites')],
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
          name='Mootiny',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='assets/misc/cows_icon.ico')

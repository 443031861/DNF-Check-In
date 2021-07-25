# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py;G:\\Dvelopment', 'Tool\\Python3.8.0\\Lib\\site-packages\\cv2', 'cv2.cp38-win_amd64.pyd'],
             pathex=['C:\\Users\\HASEE\\Desktop\\AutoDNF', 'C:\\Users\\HASEE\\Desktop\\AutoDNF'],
             binaries=[],
             datas=[],
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
          name='Dvelopment',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='sb.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Dvelopment')

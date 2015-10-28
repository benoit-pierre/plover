# -*- mode: python -*-
a = Analysis(['build/launch.py'],
             pathex=[],
             hiddenimports=[],
             hookspath=['.'],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Plover.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='windows/plover.ico')
coll = COLLECT(exe,
               a.binaries - [('mecatipia', None, None)],
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Plover')

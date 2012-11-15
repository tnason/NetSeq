# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['/Users/Andrew/school/design/NetSeq/app/gui.py'],
             pathex=['/Users/Andrew/Documents/school/2131/design/python/pyinstaller-2.0'],
             hiddenimports=[])

# TOTAL HACK: remove freetype dylib provided by Kivy and add the one from the 
# desired location on the Mac
a.binaries = a.binaries - [('libfreetype.6.dylib','','')] +\
             [('libfreetype.6.dylib', '/opt/local/lib/libfreetype.6.dylib', 
               'BINARY')]

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/netseq', 'netseq'),
          debug=False,
          strip=None,
          upx=True,
          # icon='/Users/Andrew/school/design/NetSeq/app/assets/icons/netseq-icon.icns',
          console=False )

coll = COLLECT(exe,
               [('netseq.kv', '/Users/Andrew/school/design/NetSeq/app/netseq.kv', 'DATA')],
               Tree('/Users/Andrew/school/design/NetSeq/app/assets/', prefix='assets/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'netseq'))

app = BUNDLE(coll,
             name=os.path.join('dist', 'NetSeq.app'))

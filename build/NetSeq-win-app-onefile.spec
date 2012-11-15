# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['..\\Documents\\GitHub\\NetSeq\\app\\gui.py'],
             pathex=['C:\\Users\\Work\\pyinstaller-2.0'],
             hiddenimports=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('netseq.kv', '..\\Documents\\GitHub\\NetSeq\\app\\netseq.kv', 'DATA')],
          Tree('..\\Documents\\GitHub\\NetSeq\\app\\assets\\', prefix='assets\\'),
          name=os.path.join('dist', 'NetSeq.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='..\\Documents\\GitHub\\NetSeq\\app\\assets\\icons\\netseq-icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'NetSeq.exe.app'))

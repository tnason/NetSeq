# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['..\\Documents\\GitHub\\NetSeq\\main.py'],
             pathex=['C:\\Users\\Work\\pyinstaller-2.0'],
             hiddenimports=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('netseq.kv', '..\\Documents\\GitHub\\NetSeq\\netseq\\netseq.kv', 'DATA')],
          Tree('..\\Documents\\GitHub\\NetSeq\\netseq\\sounds\\', prefix=''),
          Tree('..\\Documents\\GitHub\\NetSeq\\netseq\\images\\', prefix=''),
          name=os.path.join('dist', 'NetSeq.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='..\\Documents\\GitHub\\NetSeq\\netseq\\images\\netseq-icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'NetSeq.exe.app'))

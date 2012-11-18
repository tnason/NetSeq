# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

SOURCE_DIR = '/Users/Andrew/school/design/NetSeq/'
SCRIPT_DIR = os.path.join(SOURCE_DIR, 'netseq')

a = Analysis(['/Users/Andrew/school/design/NetSeq/main.py'],
             pathex=['/Users/Andrew/Documents/school/2131/design/python/pyinstaller-2.0'],
             hiddenimports=[])

# TOTAL HACK: remove freetype dylib provided by Kivy and add the one from the 
# desired location on the Mac
a.binaries = a.binaries - [('libfreetype.6.dylib','','')] +\
             [('libfreetype.6.dylib', '/opt/local/lib/libfreetype.6.dylib', 
               'BINARY')]

netseq_data = []
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq','netseq','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images','netseq/images','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/audio-keyboard-down.png','netseq/images/audio-keyboard-down.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/audio-keyboard.png','netseq/images/audio-keyboard.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/credits','netseq/images/credits','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/media-floppy-down.png','netseq/images/media-floppy-down.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/media-floppy.png','netseq/images/media-floppy.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/media-playback-pause-4.png','netseq/images/media-playback-pause-4.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/media-playback-start-4.png','netseq/images/media-playback-start-4.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-icon.icns','netseq/images/netseq-icon.icns','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-icon.ico','netseq/images/netseq-icon.ico','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-icon.png','netseq/images/netseq-icon.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-theme-dark.png','netseq/images/netseq-theme-dark.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-theme.atlas','netseq/images/netseq-theme.atlas','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/netseq-theme.png','netseq/images/netseq-theme.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/network-wired-2-down.png','netseq/images/network-wired-2-down.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/network-wired-2.png','netseq/images/network-wired-2.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/network-wired-4.png','netseq/images/network-wired-4.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/images/network-wireless.png','netseq/images/network-wireless.png','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds','netseq/sounds','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/chh37.ogg','netseq/sounds/chh37.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/crashedge5.ogg','netseq/sounds/crashedge5.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/hohh_15.ogg','netseq/sounds/hohh_15.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/kick_22.ogg','netseq/sounds/kick_22.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/large_tom_40-50_1.ogg','netseq/sounds/large_tom_40-50_1.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/sidestick24.ogg','netseq/sounds/sidestick24.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/small_tom_40-50_2.ogg','netseq/sounds/small_tom_40-50_2.ogg','DATA'])
# netseq_data.append(['/Users/Andrew/school/design/NetSeq/netseq/sounds/snaretop_37.ogg','netseq/sounds/snaretop_37.ogg','DATA'])

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/NetSeq', 'NetSeqApp'),
          debug=False,
          strip=None,
          upx=True,
          console=False)

coll = COLLECT(exe,
               [('netseq.kv', os.path.join(SCRIPT_DIR, 'netseq.kv'), 'DATA')],
               Tree('/Users/Andrew/school/design/NetSeq/netseq/sounds/', prefix=''),
               Tree('/Users/Andrew/school/design/NetSeq/netseq/images/', prefix=''),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'NetSeq'))

app = BUNDLE(coll,
             name=os.path.join('dist', 'NetSeq.app'))

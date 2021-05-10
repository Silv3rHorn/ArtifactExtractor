# -*- mode: python -*-

block_cipher = None


a = Analysis(['artifact_extractor.py'],
             pathex=['D:\\Dropbox\\git\\ArtifactExtractor'],
             binaries=[],
             datas=[('D:\OneDrive\git\ArtifactExtractor\\venv\Lib\site-packages\dfvfs\lib\cpio.yaml', 'dfvfs\lib'), ('D:\OneDrive\git\ArtifactExtractor\\venv\Lib\site-packages\dfvfs\lib\gzipfile.yaml', 'dfvfs\lib')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='artifact_extractor',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

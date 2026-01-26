# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resource', 'resource'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

options = [
    ('O', None, 'OPTION'),
]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    options,
    name='S.T.A.L.K.E.R. AI Quest Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resource\\icon.ico'],
)

# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

transformers_datas, transformers_binaries, transformers_hiddenimports = collect_all(
    'transformers'
)

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[
        *transformers_binaries,
    ],
    datas=[
        ('resource', 'resource'),
        *transformers_datas,
    ],
    hiddenimports=[
        *transformers_hiddenimports,
    ],
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

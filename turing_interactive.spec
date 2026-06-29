# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Turing Interactive Application
Builds a standalone executable that loads the Turing Model and engages users.
"""

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Data files to include (model configs, trained events)
datas = [
    ('model.json', '.'),
    ('trained_turing_events.json', '.'),
    ('data', 'data'),
]

# Include the adrenaline_turing_model package
datas += collect_data_files('adrenaline_turing_model')

a = Analysis(
    ['turing_interactive.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['adrenaline_turing_model', 'adrenaline_turing_model.model'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TuringInteractive',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

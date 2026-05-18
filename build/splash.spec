# PyInstaller spec — build a single-file executable for Splash.
# Usage: pyinstaller build/splash.spec
# Linux + Windows  → single executable in dist/
# macOS            → Splash.app bundle in dist/
import sys
from PyInstaller.utils.hooks import collect_submodules

IS_MAC = sys.platform == "darwin"

block_cipher = None
hidden = collect_submodules("converter")

a = Analysis(
    ["../run.py"],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "test", "unittest"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Splash",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX shrinks Linux/Windows binaries; it corrupts macOS .app bundles.
    upx=not IS_MAC,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

if IS_MAC:
    app = BUNDLE(
        exe,
        name="Splash.app",
        icon=None,
        bundle_identifier="com.splash.videoconverter",
        info_plist={
            "CFBundleName": "Splash",
            "CFBundleDisplayName": "Splash",
            "CFBundleShortVersionString": "1.0.0",
            "CFBundleVersion": "1.0.0",
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "11.0",
            "NSHumanReadableCopyright": "© 2026 Mohamed Aly Sayed",
        },
    )

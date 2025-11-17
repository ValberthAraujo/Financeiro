# -*- mode: python ; coding: utf-8 -*-
import site
import sys
from pathlib import Path

block_cipher = None

SPEC_PATH = Path(globals().get("__file__", sys.argv[0])).resolve()
PROJECT_ROOT = SPEC_PATH.parent
APP_DIR = PROJECT_ROOT / "app"
VIEW_DIR = APP_DIR / "view"
ASSETS_DIR = PROJECT_ROOT / "assets"


def collect_tree(source: Path, target_root: Path):
    entries = []
    if not source.exists():
        return entries
    for item in source.rglob("*"):
        if item.is_file():
            relative = item.relative_to(source)
            destination_dir = target_root / relative.parent
            entries.append((str(item), str(destination_dir)))
    return entries


datas = collect_tree(VIEW_DIR, Path("app") / "view")
datas += collect_tree(ASSETS_DIR, Path("assets"))

env_file = PROJECT_ROOT / "init.env"
if env_file.exists():
    datas.append((str(env_file), "init.env"))


def collect_kivy_deps(*deps):
    collected = []
    for dep_name in deps:
        for package_dir in site.getsitepackages():
            candidate = Path(package_dir) / "kivy_deps" / dep_name
            if candidate.exists():
                collected += collect_tree(candidate, Path("kivy_deps") / dep_name)
                break
    return collected


datas += collect_kivy_deps("sdl2", "glew", "gstreamer", "angle")

hiddenimports = [
    "kivy.core.window.window_sdl2",
    "kivy.core.audio.audio_sdl2",
    "kivy.core.text.text_sdl2",
    "kivy.core.video.video_ffpyplayer",
    "kivy.core.image.img_sdl2",
    "kivy.modules",
    "pdfplumber",
]

a = Analysis(
    ["app/main.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="controle_financeiro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJECT_ROOT / "assets" / "icon.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="controle_financeiro",
)

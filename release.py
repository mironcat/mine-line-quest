#!/usr/bin/env python
"""Сборка релизного exe для MINE-LINE.

Запуск из корня проекта:
    python release.py            # собрать dist/mine-line-quest.exe
    python release.py --no-install
    python release.py -- --log-level=WARN   # доп. аргументы PyInstaller

Если PyInstaller не установлен, скрипт поставит его сам (кроме --no-install).
"""
import importlib.util
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "make_exe.spec"
APP_NAME = "mine-line-quest"
EXE = ROOT / "dist" / f"{APP_NAME}.exe"
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"


def log(message=""):
    print(message, flush=True)


def run(cmd):
    log("> " + " ".join(str(part) for part in cmd))
    subprocess.run([str(part) for part in cmd], cwd=ROOT, check=True)


def pyinstaller_version():
    try:
        import PyInstaller
    except ImportError:
        return None
    return PyInstaller.__version__


def ensure_pyinstaller(auto_install):
    version = pyinstaller_version()
    if version:
        log(f"PyInstaller: {version}")
        return
    if not auto_install:
        sys.exit("PyInstaller не установлен. Выполните: python -m pip install pyinstaller")
    log("PyInstaller не найден, устанавливаю...")
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])


def clean():
    for folder in (BUILD_DIR, DIST_DIR):
        if folder.exists():
            try:
                shutil.rmtree(folder)
            except OSError as error:
                sys.exit(f"Не удалось удалить {folder}: {error}\nЗакройте запущенную игру и повторите.")
            log(f"Удалено: {folder}")


def build(extra_args):
    run([sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", SPEC, *extra_args])


def report(started):
    if not EXE.is_file():
        sys.exit(f"Сборка завершилась, но файл не найден: {EXE}")
    size_mb = EXE.stat().st_size / (1024 * 1024)
    log()
    log("Готово!")
    log(f"Файл:   {EXE}")
    log(f"Размер: {size_mb:.1f} МБ")
    log(f"Время:  {time.monotonic() - started:.1f} с")


def main(argv):
    args = list(argv)
    auto_install = "--no-install" not in args
    args = [arg for arg in args if arg != "--no-install"]
    extra_args = args[args.index("--") + 1:] if "--" in args else args

    started = time.monotonic()

    if not SPEC.is_file():
        sys.exit(f"Не найден {SPEC.name}. Запускайте релиз из корня проекта.")
    log("=== Сборка MINE-LINE ===")
    log(f"Python: {sys.version.split()[0]}")
    ensure_pyinstaller(auto_install)
    clean()
    build(extra_args)
    report(started)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except subprocess.CalledProcessError as error:
        sys.exit(f"Ошибка сборки (код {error.returncode}). Подробности выше.")
    except KeyboardInterrupt:
        sys.exit("Сборка прервана.")

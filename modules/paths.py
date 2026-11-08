import os
import sys

# Корень проекта: папка, в которой лежат heroes/, screens/ и start_game.py
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_path(path):
    """Путь к ресурсу и в исходниках, и внутри собранного exe.

    При сборке PyInstaller кладёт heroes/ и screens/ во временную папку
    sys._MEIPASS, поэтому относительные пути нельзя открывать напрямую.
    """
    if os.path.isabs(path):
        return path
    base = getattr(sys, '_MEIPASS', PROJECT_ROOT)
    return os.path.join(base, path)

"""Launcher ejecutable para DeskPets.

Este ejecutable corre el código fuente ubicado en ./app, para que cambios
sobre archivos .py instalados se reflejen al reiniciar la app.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import PySide6  # noqa: F401  # Fuerza inclusión de dependencia en build
import pynput  # noqa: F401  # Fuerza inclusión de dependencia en build


def _resolve_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def main() -> None:
    base_dir = _resolve_base_dir()
    app_dir = base_dir / "app"
    entrypoint = app_dir / "main.py"

    if not entrypoint.exists():
        raise FileNotFoundError(
            f"No se encontró {entrypoint}. Reinstala DeskPets o verifica la carpeta app/."
        )

    sys.path.insert(0, str(app_dir))
    runpy.run_path(str(entrypoint), run_name="__main__")


if __name__ == "__main__":
    main()

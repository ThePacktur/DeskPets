"""Clases y utilidades visuales de mascotas para DeskPets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap

TIPOS_MASCOTA = ("gato", "cactus", "pato")
TAMANOS = {
    "pequeno": 96,
    "mediano": 128,
    "grande": 168,
}


def _canvas(size: int) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(0, 0, 0, 0))
    return pixmap


def _pen() -> QPen:
    pen = QPen(QColor("#1f1f1f"))
    pen.setWidth(3)
    return pen


def _draw_cat(p: QPainter, skin: str, frame: int, size: int) -> None:
    base = QColor("#f6b26b") if skin == "normal" else QColor("#d8a7ff")
    belly = QColor("#ffe6cc") if skin == "normal" else QColor("#efe0ff")

    body_y = int(size * (0.31 + (0.01 if frame % 2 == 0 else 0.0)))
    p.setBrush(base)
    p.drawRoundedRect(QRect(int(size * 0.2), body_y, int(size * 0.6), int(size * 0.5)), 18, 18)

    p.drawPolygon(
        [
            QPoint(int(size * 0.28), int(size * 0.24)),
            QPoint(int(size * 0.36), int(size * 0.08)),
            QPoint(int(size * 0.43), int(size * 0.24)),
        ]
    )
    p.drawPolygon(
        [
            QPoint(int(size * 0.57), int(size * 0.24)),
            QPoint(int(size * 0.64), int(size * 0.08)),
            QPoint(int(size * 0.72), int(size * 0.24)),
        ]
    )

    p.setBrush(belly)
    p.drawEllipse(QRect(int(size * 0.36), int(size * 0.49), int(size * 0.28), int(size * 0.22)))

    eye_open = frame != 1
    p.setBrush(QColor("#1f1f1f"))
    if eye_open:
        p.drawEllipse(QRect(int(size * 0.37), int(size * 0.35), 8, 8))
        p.drawEllipse(QRect(int(size * 0.55), int(size * 0.35), 8, 8))
    else:
        p.drawLine(int(size * 0.35), int(size * 0.39), int(size * 0.43), int(size * 0.39))
        p.drawLine(int(size * 0.53), int(size * 0.39), int(size * 0.61), int(size * 0.39))

    p.setBrush(QColor("#ff8fab"))
    p.drawEllipse(QRect(int(size * 0.47), int(size * 0.41), 9, 7))


def _draw_cactus(p: QPainter, skin: str, frame: int, size: int) -> None:
    green = QColor("#6aa84f") if skin == "normal" else QColor("#4ecdc4")
    pot = QColor("#b45f06") if skin == "normal" else QColor("#8d5a97")

    sway = -2 if frame == 0 else (2 if frame == 2 else 0)

    p.setBrush(green)
    p.drawRoundedRect(QRect(int(size * 0.38) + sway, int(size * 0.2), int(size * 0.24), int(size * 0.5)), 14, 14)
    p.drawRoundedRect(QRect(int(size * 0.25) + sway, int(size * 0.34), int(size * 0.12), int(size * 0.24)), 10, 10)
    p.drawRoundedRect(QRect(int(size * 0.63) + sway, int(size * 0.36), int(size * 0.12), int(size * 0.24)), 10, 10)

    p.setPen(QPen(QColor("#f0f0f0"), 2))
    for y in range(int(size * 0.24), int(size * 0.66), int(size * 0.08)):
        p.drawPoint(int(size * 0.44) + sway, y)
        p.drawPoint(int(size * 0.56) + sway, y)
    p.setPen(_pen())

    p.setBrush(pot)
    p.drawRoundedRect(QRect(int(size * 0.23), int(size * 0.68), int(size * 0.54), int(size * 0.18)), 10, 10)


def _draw_duck(p: QPainter, skin: str, frame: int, size: int) -> None:
    body = QColor("#ffd966") if skin == "normal" else QColor("#b6f0ff")
    beak = QColor("#f6b26b") if skin == "normal" else QColor("#ff7aa2")

    bob = 2 if frame == 1 else 0

    p.setBrush(body)
    p.drawEllipse(QRect(int(size * 0.2), int(size * 0.32) + bob, int(size * 0.58), int(size * 0.4)))
    p.drawEllipse(QRect(int(size * 0.56), int(size * 0.2) + bob, int(size * 0.22), int(size * 0.22)))

    p.setBrush(QColor("#1f1f1f"))
    p.drawEllipse(QRect(int(size * 0.64), int(size * 0.28) + bob, 7, 7))

    p.setBrush(beak)
    p.drawRoundedRect(QRect(int(size * 0.74), int(size * 0.31) + bob, int(size * 0.14), int(size * 0.08)), 4, 4)

    p.setBrush(QColor("#ffef99") if skin == "normal" else QColor("#d8fbff"))
    p.drawEllipse(QRect(int(size * 0.32), int(size * 0.42) + bob, int(size * 0.24), int(size * 0.16)))


@dataclass
class MascotaFrames:
    """Agrupa los frames de animación de una mascota/skin/tamaño."""

    frames: List[QPixmap]


class FabricaMascotas:
    """Generador en memoria de sprites simples estilo pixel/cartoon."""

    def __init__(self) -> None:
        self._cache: Dict[Tuple[str, str, str], MascotaFrames] = {}

    def obtener_frames(self, mascota: str, skin: str, tamano: str) -> List[QPixmap]:
        clave = (mascota, skin, tamano)
        if clave in self._cache:
            return self._cache[clave].frames

        size = TAMANOS[tamano]
        frames: List[QPixmap] = []

        for frame in range(3):
            pixmap = _canvas(size)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(_pen())

            if mascota == "gato":
                _draw_cat(painter, skin, frame, size)
            elif mascota == "cactus":
                _draw_cactus(painter, skin, frame, size)
            else:
                _draw_duck(painter, skin, frame, size)

            painter.end()
            frames.append(pixmap)

        self._cache[clave] = MascotaFrames(frames=frames)
        return frames

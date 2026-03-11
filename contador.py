"""Módulo de contador global de puntos para DeskPets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContadorPuntos:
    """Gestiona el puntaje acumulado por interacción del usuario."""

    puntos: int = 0

    def agregar_click(self) -> int:
        """Suma un punto por click sobre la mascota."""
        self.puntos += 1
        return self.puntos

    def agregar_tecla(self) -> int:
        """Suma un punto por cada tecla presionada de forma global."""
        self.puntos += 1
        return self.puntos

    def obtener(self) -> int:
        """Retorna el puntaje actual."""
        return self.puntos

    def fijar(self, nuevo_valor: int) -> None:
        """Actualiza el contador con un valor persistido."""
        self.puntos = max(0, int(nuevo_valor))

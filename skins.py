"""Gestión de skins y desbloqueo por puntos para DeskPets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

UMBRAL_DESBLOQUEO = 10_000
TIPOS_MASCOTA = ("gato", "cactus", "pato")


@dataclass
class GestorSkins:
    """Administra el estado de desbloqueo y skin activa."""

    skin_actual: str = "normal"
    desbloqueadas: Dict[str, bool] = field(
        default_factory=lambda: {"gato": False, "cactus": False, "pato": False}
    )

    def actualizar_por_puntos(self, puntos: int) -> bool:
        """Desbloquea skins al alcanzar el umbral. Retorna True si hubo cambios."""
        if puntos < UMBRAL_DESBLOQUEO:
            return False

        hubo_cambios = False
        for mascota in TIPOS_MASCOTA:
            if not self.desbloqueadas.get(mascota, False):
                self.desbloqueadas[mascota] = True
                hubo_cambios = True
        return hubo_cambios

    def opciones_skin(self, mascota: str) -> list[str]:
        """Retorna skins disponibles para una mascota."""
        opciones = ["normal"]
        if self.desbloqueadas.get(mascota, False):
            opciones.append("especial")
        return opciones

    def puede_usar(self, mascota: str, skin: str) -> bool:
        """Valida si una skin puede usarse en la mascota indicada."""
        if skin == "normal":
            return True
        return skin == "especial" and self.desbloqueadas.get(mascota, False)

    def fijar_skin(self, mascota: str, skin: str) -> str:
        """Intenta activar una skin válida; devuelve la skin finalmente activa."""
        if self.puede_usar(mascota, skin):
            self.skin_actual = skin
        else:
            self.skin_actual = "normal"
        return self.skin_actual

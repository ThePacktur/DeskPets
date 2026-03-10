"""Aplicación principal de DeskPets."""

from __future__ import annotations

import json
import random
import sys
import threading
from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, QTimer, Qt, Signal, QObject
from PySide6.QtGui import QAction, QCursor, QMouseEvent
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu
from pynput import keyboard

from contador import ContadorPuntos
from mascotas import FabricaMascotas, TAMANOS, TIPOS_MASCOTA
from skins import GestorSkins

CONFIG_PATH = Path(__file__).with_name("config.json")
DEFAULT_CONFIG = {
    "mascota_actual": "gato",
    "skin_actual": "normal",
    "tamano": "mediano",
    "puntos": 0,
    "siempre_encima": True,
    "skins_desbloqueadas": {
        "gato": False,
        "cactus": False,
        "pato": False,
    },
}


class KeySignalEmitter(QObject):
    """Emite señal Qt por cada tecla capturada globalmente."""

    key_pressed = Signal()


class DeskPetWindow(QMainWindow):
    """Ventana transparente sin bordes que dibuja y anima la mascota."""

    def __init__(self) -> None:
        super().__init__()

        self.config = self._load_config()
        self.contador = ContadorPuntos(self.config["puntos"])
        self.skins = GestorSkins(
            skin_actual=self.config["skin_actual"],
            desbloqueadas=self.config["skins_desbloqueadas"],
        )
        self.fabrica = FabricaMascotas()

        self.mascota_actual = self.config["mascota_actual"]
        self.tamano_actual = self.config["tamano"]
        self.frame_index = 0
        self.drag_offset = QPoint()
        self.dragging = False

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
            if self.config["siempre_encima"]
            else Qt.FramelessWindowHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

        self.pet_label = QLabel(self)
        self.pet_label.setStyleSheet("background: transparent;")

        self.points_label = QLabel(self)
        self.points_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                background-color: rgba(0,0,0,130);
                border-radius: 8px;
                padding: 3px 7px;
                font-size: 11px;
                font-weight: bold;
            }
            """
        )

        self.effect_label = QLabel(self)
        self.effect_label.setStyleSheet("color: #ff4fa3; font-size: 22px; font-weight: bold;")
        self.effect_label.hide()

        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.next_frame)
        self.anim_timer.start(300)

        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.show_random_tip)
        self.message_timer.start(9000)

        self.sleep_timer = QTimer(self)
        self.sleep_timer.timeout.connect(self.enter_sleep_mode)
        self.sleep_timer.setSingleShot(True)
        self.sleep_timer.start(25000)

        self.is_sleeping = False
        self.messages = [
            "¡Hoy brillas!",
            "Un click y seguimos ✨",
            "DeskPets te acompaña",
            "¡Gracias por jugar conmigo!",
        ]

        self.key_emitter = KeySignalEmitter()
        self.key_emitter.key_pressed.connect(self.on_global_key)
        self._start_keyboard_listener()

        self._load_frames()
        self.refresh_ui()
        self.move(200, 200)

    def _start_keyboard_listener(self) -> None:
        def on_press(_key: object) -> None:
            self.key_emitter.key_pressed.emit()

        listener = keyboard.Listener(on_press=on_press)
        thread = threading.Thread(target=listener.run, daemon=True)
        thread.start()

    def _load_config(self) -> dict:
        if CONFIG_PATH.exists():
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            merged["skins_desbloqueadas"] = {
                **DEFAULT_CONFIG["skins_desbloqueadas"],
                **data.get("skins_desbloqueadas", {}),
            }
            return merged

        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG.copy()

    def _save_config(self) -> None:
        payload = {
            "mascota_actual": self.mascota_actual,
            "skin_actual": self.skins.skin_actual,
            "tamano": self.tamano_actual,
            "puntos": self.contador.obtener(),
            "siempre_encima": bool(self.windowFlags() & Qt.WindowStaysOnTopHint),
            "skins_desbloqueadas": self.skins.desbloqueadas,
        }
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)

    def _load_frames(self) -> None:
        self.frames = self.fabrica.obtener_frames(self.mascota_actual, self.skins.skin_actual, self.tamano_actual)

    def refresh_ui(self) -> None:
        pix = self.frames[self.frame_index % len(self.frames)]
        self.pet_label.setPixmap(pix)
        self.pet_label.resize(pix.size())
        self.resize(pix.size())
        self.points_label.setText(f"Puntos: {self.contador.obtener()}")
        self.points_label.adjustSize()
        self.points_label.move(8, 8)
        self.setToolTip(f"{self.mascota_actual.title()} | {self.skins.skin_actual} | Puntos: {self.contador.obtener()}")
        self.update()

    def next_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.refresh_ui()

    def add_point_click(self) -> None:
        self.contador.agregar_click()
        self.post_point_update()
        self.show_click_effect("❤")

    def on_global_key(self) -> None:
        self.contador.agregar_tecla()
        self.post_point_update()

    def post_point_update(self) -> None:
        unlocked_now = self.skins.actualizar_por_puntos(self.contador.obtener())
        if unlocked_now:
            self.showMessage(
                "DeskPets",
                "🎉 ¡Desbloqueaste skins especiales para Gato, Cactus y Pato!",
                5000,
            )
        self.is_sleeping = False
        self.sleep_timer.start(25000)
        self.refresh_ui()

    def show_click_effect(self, text: str) -> None:
        self.effect_label.setText(text)
        self.effect_label.adjustSize()
        self.effect_label.move(int(self.width() * 0.45), int(self.height() * 0.25))
        self.effect_label.show()
        QTimer.singleShot(350, self.effect_label.hide)

    def show_random_tip(self) -> None:
        self.setToolTip(f"{random.choice(self.messages)}\nPuntos: {self.contador.obtener()}")

    def enter_sleep_mode(self) -> None:
        self.is_sleeping = True
        self.setToolTip(f"{self.mascota_actual.title()} está dormid@... Zzz")

    def contextMenuEvent(self, _event: QEvent) -> None:
        menu = QMenu(self)

        menu.addSection("Mascota")
        for mascota in TIPOS_MASCOTA:
            action = QAction(mascota.title(), self, checkable=True)
            action.setChecked(self.mascota_actual == mascota)
            action.triggered.connect(lambda checked=False, m=mascota: self.change_mascota(m))
            menu.addAction(action)

        menu.addSection("Tamaño")
        for key, label in (("pequeno", "Pequeño"), ("mediano", "Mediano"), ("grande", "Grande")):
            action = QAction(label, self, checkable=True)
            action.setChecked(self.tamano_actual == key)
            action.triggered.connect(lambda checked=False, t=key: self.change_size(t))
            menu.addAction(action)

        menu.addSection("Skin")
        for skin in self.skins.opciones_skin(self.mascota_actual):
            action = QAction(skin.title(), self, checkable=True)
            action.setChecked(self.skins.skin_actual == skin)
            action.triggered.connect(lambda checked=False, s=skin: self.change_skin(s))
            menu.addAction(action)

        menu.addSeparator()
        points_action = QAction(f"Ver contador: {self.contador.obtener()} puntos", self)
        points_action.setEnabled(False)
        menu.addAction(points_action)

        always_on_top = QAction("Siempre encima", self, checkable=True)
        always_on_top.setChecked(bool(self.windowFlags() & Qt.WindowStaysOnTopHint))
        always_on_top.triggered.connect(self.toggle_on_top)
        menu.addAction(always_on_top)

        close_action = QAction("Cerrar", self)
        close_action.triggered.connect(self.close)
        menu.addAction(close_action)

        menu.exec(QCursor.pos())

    def change_mascota(self, mascota: str) -> None:
        self.mascota_actual = mascota
        if not self.skins.puede_usar(mascota, self.skins.skin_actual):
            self.skins.skin_actual = "normal"
        self._load_frames()
        self.refresh_ui()

    def change_size(self, tamano: str) -> None:
        self.tamano_actual = tamano
        self._load_frames()
        self.refresh_ui()

    def change_skin(self, skin: str) -> None:
        self.skins.fijar_skin(self.mascota_actual, skin)
        self._load_frames()
        self.refresh_ui()

    def toggle_on_top(self) -> None:
        currently_top = bool(self.windowFlags() & Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, not currently_top)
        self.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.add_point_click()
            event.accept()
        elif event.button() == Qt.RightButton:
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, _event: QMouseEvent) -> None:
        self.dragging = False

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self._save_config()
        event.accept()


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    window = DeskPetWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

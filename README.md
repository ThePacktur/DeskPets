# DeskPets — Mascota Virtual de Escritorio para Windows

**DeskPets** es una aplicación ligera y adorable que agrega una mascota animada flotante sobre tu escritorio.

Convierte tus clics y tu actividad de teclado en puntos, desbloquea skins especiales y personaliza tu compañero virtual para que refleje tu estilo.

---

## ✨ ¿Qué ofrece DeskPets?

- **3 mascotas únicas**: Gato, Cactus y Pato.
- **Animación continua** por frames para dar sensación de vida.
- **Sistema de puntos global**:
  - +1 por cada click sobre la mascota.
  - +1 por cada tecla presionada (captura global).
- **Desbloqueo de skins** al llegar a **10,000 puntos** (para cada mascota).
- **Menú contextual completo** (clic derecho):
  - Cambiar mascota.
  - Cambiar tamaño (pequeño/mediano/grande).
  - Cambiar skin (normal/especial si ya está desbloqueada).
  - Ver contador actual.
  - Alternar “siempre encima”.
  - Cerrar aplicación.
- **Ventana sin bordes**, con fondo transparente y arrastre libre por pantalla.
- **Persistencia automática** en `config.json`.
- Extras incluidos:
  - Efecto visual al click (corazón).
  - Tooltips con mensajes aleatorios.
  - Modo inactivo/dormido tras un tiempo sin interacción.

---

## 🧩 Tecnologías

- **Python 3.10+**
- **PySide6** (interfaz y transparencia)
- **pynput** (captura global de teclado)

---

## 📁 Estructura del proyecto

- `main.py` → Arranque de app, ventana principal, interacción, persistencia.
- `mascotas.py` → Clases de mascotas y generación de animaciones por frames.
- `contador.py` → Sistema de puntos global.
- `skins.py` → Gestión de skins y desbloqueo por umbral.
- `config.json` → Preferencias y progreso del usuario.

---

## 🚀 Instalación y ejecución

### 1) Clonar o descargar

Descarga el proyecto en una carpeta local.

### 2) Crear entorno virtual (recomendado)

```bash
python -m venv .venv
```

Activar en Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3) Instalar dependencias

```bash
pip install PySide6 pynput
```

### 4) Ejecutar

```bash
python main.py
```

---

## 🛠️ Personalización y escalabilidad

DeskPets está diseñado para crecer fácilmente:

- Puedes añadir nuevas mascotas extendiendo la lógica en `mascotas.py`.
- Puedes crear más skins reutilizando el sistema de `skins.py`.
- Puedes modificar el umbral de desbloqueo desde `skins.py` (`UMBRAL_DESBLOQUEO`).
- Puedes ajustar mensajes, tiempos de animación y comportamiento de inactividad en `main.py`.

---

## 💼 Enfoque comercial

DeskPets es ideal para:

- Usuarios que quieren personalizar su escritorio sin consumir muchos recursos.
- Streamers y creadores de contenido que buscan identidad visual en pantalla.
- Equipos de trabajo que desean una experiencia más agradable durante largas jornadas.

Su diseño modular permite evolucionar rápidamente hacia ediciones premium con:

- Packs de skins temáticos.
- Mascotas coleccionables.
- Eventos de temporada.
- Integraciones con productividad/gamificación.

---

## 📌 Nota

La función de inicio automático con Windows puede agregarse como extensión futura (registro o acceso directo en carpeta de inicio), manteniendo la app base limpia y liviana.

¡Disfruta tu DeskPet! 🐾

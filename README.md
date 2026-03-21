# DeskPets — Mascota Virtual de Escritorio para Windows

**DeskPets** es una aplicación ligera y adorable que agrega una mascota animada flotante sobre tu escritorio.

Convierte tus clics y tu actividad de teclado en puntos, desbloquea skins especiales y personaliza tu compañero virtual para que refleje tu estilo.

---

## ✨ ¿Qué ofrece DeskPets?

- **3 mascotas únicas**: **Kaliko (gato)**, Cactus y Pato.
- **Animación continua** por frames para dar sensación de vida.
- **Kaliko con sprites PNG** (despierto + modo dormido con 3 poses).
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
- `mascotas.py` → Clases de mascotas y generación/carga de animaciones por frames.
- `contador.py` → Sistema de puntos global.
- `skins.py` → Gestión de skins y desbloqueo por umbral.
- `config.json` → Preferencias y progreso del usuario.
- `assets/kaliko/` → Carpeta de sprites PNG de Kaliko.

---

## 🐱 Integración de Kaliko (sprites)

Coloca los PNG en `assets/kaliko/` con estos nombres exactos:

- `kaliko_idle.png`
- `kaliko_sleep_1.png`
- `kaliko_sleep_2.png`
- `kaliko_Idle1.png`

Si no están presentes, la app usa un dibujo interno de respaldo para el gato.

---

## 🚀 Instalación y ejecución

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install PySide6 pynput
```

Ejecutar:

```bash
python main.py
```

---

## 💼 Enfoque comercial

DeskPets es ideal para usuarios que quieren personalizar su escritorio sin consumir muchos recursos, creadores de contenido y equipos que buscan una experiencia más agradable.

Su arquitectura modular permite crecer fácilmente con packs de skins, mascotas coleccionables, eventos de temporada e integraciones de gamificación.

---

## 🏗️ Crear ejecutable + instalador (Windows)

### 1) Generar ejecutable

Desde PowerShell en la raíz del proyecto:

```powershell
./scripts/build_windows.ps1 -Clean
```

Esto genera:

- `dist/DeskPets/DeskPets.exe` (ejecutable)
- `dist/DeskPets/app/` (código fuente editable que usa el ejecutable)

> DeskPets.exe está preparado para ejecutar `app/main.py` en cada inicio.
> Si editas `app/*.py` dentro de la instalación, los cambios se aplican al reiniciar la app.

### 2) Crear instalador `.exe` (Inno Setup)

1. Instala **Inno Setup 6**.
2. Abre `installer/DeskPets.iss`.
3. Compila el script (`Build -> Compile`).

Resultado esperado:

- `dist/DeskPets-Installer.exe`

### 3) Flujo para aplicar cambios de código en una app ya instalada

La instalación queda en:

- `%LOCALAPPDATA%\DeskPets\app`

Opciones:

- Editar directamente los `.py` en esa carpeta, y reiniciar DeskPets.
- O sincronizar desde este repo con:

```powershell
./scripts/sync_installed_code.ps1
```

Si instalaste en otra ruta:

```powershell
./scripts/sync_installed_code.ps1 -InstallPath "D:\Apps\DeskPets"
```

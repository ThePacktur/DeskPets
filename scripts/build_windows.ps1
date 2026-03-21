Param(
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path "$PSScriptRoot/..")

if ($Clean) {
    Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
}

python -m pip install --upgrade pip
python -m pip install pyinstaller PySide6 pynput

pyinstaller --noconfirm --clean --windowed --onedir --name DeskPets launcher.py

$targetAppDir = 'dist/DeskPets/app'
New-Item -ItemType Directory -Force -Path $targetAppDir | Out-Null

Copy-Item main.py,mascotas.py,skins.py,contador.py,config.json -Destination $targetAppDir -Force
Copy-Item assets -Destination $targetAppDir -Recurse -Force

Write-Host ''
Write-Host 'Build completado:'
Write-Host '  dist/DeskPets/DeskPets.exe'
Write-Host '  dist/DeskPets/app/*.py (editable para aplicar cambios)'

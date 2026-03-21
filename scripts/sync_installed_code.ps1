Param(
    [string]$InstallPath = "$env:LOCALAPPDATA\DeskPets"
)

$ErrorActionPreference = 'Stop'
$repoRoot = Resolve-Path "$PSScriptRoot/.."
$appPath = Join-Path $InstallPath 'app'

if (!(Test-Path $appPath)) {
    throw "No existe la ruta instalada: $appPath"
}

Copy-Item "$repoRoot/main.py","$repoRoot/mascotas.py","$repoRoot/skins.py","$repoRoot/contador.py" -Destination $appPath -Force
Copy-Item "$repoRoot/assets" -Destination $appPath -Recurse -Force

Write-Host "Código sincronizado en: $appPath"
Write-Host 'Reinicia DeskPets para ver los cambios.'

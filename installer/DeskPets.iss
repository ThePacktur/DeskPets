#define MyAppName "DeskPets"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DeskPets"
#define MyAppURL "https://example.com"
#define MyAppExeName "DeskPets.exe"

[Setup]
AppId={{9D0D4A4B-5626-4D3A-A8E8-7F8B0B1F7D66}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={localappdata}\DeskPets
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=DeskPets-Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "..\dist\DeskPets\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\DeskPets"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\DeskPets"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar DeskPets"; Flags: nowait postinstall skipifsilent

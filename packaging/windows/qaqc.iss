; LogiQore Reporter Windows installer script (Inno Setup 6)
; Usage:
;   1) Build executables first: python scripts/build_executables.py --target all --clean
;   2) Build installer: ISCC.exe packaging\windows\qaqc.iss

#define MyAppName "LogiQore Reporter"
#define MyAppVersion "1.0.0-pre"
#define MyAppPublisher "LogiQore"
#define MyAppExeName "LogiQore-Reporter-GUI.exe"
#define MyCliExeName "LogiQore-Reporter-CLI.exe"

[Setup]
AppId={{E9E8A0D6-8CEB-4B3B-B662-92A2D45C0C0A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\LogiQore Reporter
DefaultGroupName=LogiQore Reporter
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Core executables
Source: "dist\gui\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\cli\{#MyCliExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Runtime config and reference data
Source: "config.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "crm_database.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "mock_data\*"; DestDir: "{app}\mock_data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\LogiQore Reporter"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\LogiQore Reporter CLI Command Prompt"; Filename: "{cmd}"; Parameters: "/k cd /d \"{app}\""
Name: "{autodesktop}\LogiQore Reporter"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch LogiQore Reporter"; Flags: nowait postinstall skipifsilent

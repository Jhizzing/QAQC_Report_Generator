; QAQC Windows installer script (Inno Setup 6)
; Usage:
;   1) Build executables first: python scripts/build_executables.py --target all --clean
;   2) Build installer: ISCC.exe packaging\windows\qaqc.iss

#define MyAppName "QAQC Analysis Application"
#define MyAppVersion "1.0.0-pre"
#define MyAppPublisher "LogiQore"
#define MyAppExeName "QAQC-GUI.exe"
#define MyCliExeName "QAQC-CLI.exe"

[Setup]
AppId={{E9E8A0D6-8CEB-4B3B-B662-92A2D45C0C0A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\QAQC
DefaultGroupName=QAQC
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
Name: "{autoprograms}\QAQC GUI"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\QAQC CLI Command Prompt"; Filename: "{cmd}"; Parameters: "/k cd /d \"{app}\""
Name: "{autodesktop}\QAQC GUI"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch QAQC GUI"; Flags: nowait postinstall skipifsilent

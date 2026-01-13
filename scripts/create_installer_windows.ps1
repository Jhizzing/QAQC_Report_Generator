# Create Windows installer using Inno Setup
# Requires Inno Setup to be installed: https://jrsoftware.org/isinfo.php

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$DistDir = Join-Path $ProjectRoot "dist"
$PackagingDir = Join-Path $ProjectRoot "packaging"
$InnoSetupDir = Join-Path $PackagingDir "windows"

Write-Host "Creating Windows installer..."

# Check if GUI executable exists
$GuiExe = Join-Path $DistDir "gui\QAQC-GUI.exe"
if (-not (Test-Path $GuiExe)) {
    Write-Host "Error: GUI executable not found at $GuiExe"
    Write-Host "Please build the executable first: python scripts/build_executables.py --target gui"
    exit 1
}

# Check for Inno Setup
$InnoSetupCompiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (-not (Test-Path $InnoSetupCompiler)) {
    $InnoSetupCompiler = "C:\Program Files\Inno Setup 6\ISCC.exe"
}

if (-not (Test-Path $InnoSetupCompiler)) {
    Write-Host "Error: Inno Setup not found"
    Write-Host "Please install Inno Setup from: https://jrsoftware.org/isinfo.php"
    exit 1
}

# Create Inno Setup script if it doesn't exist
$InnoScript = Join-Path $InnoSetupDir "qaqc.iss"
if (-not (Test-Path $InnoScript)) {
    Write-Host "Creating Inno Setup script..."
    New-Item -ItemType Directory -Force -Path $InnoSetupDir | Out-Null
    
    $InnoScriptContent = @"
[Setup]
AppName=QAQC Report Generator
AppVersion=1.0.0
DefaultDirName={pf}\QAQC Report Generator
DefaultGroupName=QAQC Report Generator
OutputDir=$DistDir
OutputBaseFilename=QAQC-GUI-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=
LicenseFile=
WizardStyle=modern

[Files]
Source: "$DistDir\gui\QAQC-GUI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "$ProjectRoot\config.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "$ProjectRoot\crm_database.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "$ProjectRoot\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs
Source: "$ProjectRoot\mock_data\*"; DestDir: "{app}\mock_data"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\QAQC Report Generator"; Filename: "{app}\QAQC-GUI.exe"
Name: "{group}\Uninstall QAQC Report Generator"; Filename: "{uninstallexe}"
Name: "{commondesktop}\QAQC Report Generator"; Filename: "{app}\QAQC-GUI.exe"

[Run]
Filename: "{app}\QAQC-GUI.exe"; Description: "Launch QAQC Report Generator"; Flags: nowait postinstall skipifsilent
"@
    
    Set-Content -Path $InnoScript -Value $InnoScriptContent
}

# Compile installer
Write-Host "Compiling installer with Inno Setup..."
& $InnoSetupCompiler $InnoScript

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Windows installer created successfully!"
    Write-Host "Installer location: $DistDir\QAQC-GUI-Setup.exe"
} else {
    Write-Host "❌ Installer compilation failed"
    exit 1
}

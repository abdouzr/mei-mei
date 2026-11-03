[Setup]
AppName=mei mei
AppVersion=1.0
DefaultDirName={autopf}\mei mei
DefaultGroupName=mei mei
PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename=MeiMei-Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\MeiMei.exe

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"

[Files]
Source: "dist\MeiMei\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\mei mei"; Filename: "{app}\MeiMei.exe"
Name: "{autodesktop}\mei mei"; Filename: "{app}\MeiMei.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MeiMei.exe"; Description: "Launch mei mei"; Flags: nowait postinstall skipifsilent

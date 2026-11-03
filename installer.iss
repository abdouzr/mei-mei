[Setup]
AppName=mei mei
AppVersion=1.0
DefaultDirName={autopf}\mei mei
DefaultGroupName=mei mei
PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename=mei mei Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\mei mei.exe

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"

[Files]
Source: "dist\mei mei\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\mei mei"; Filename: "{app}\mei mei.exe"
Name: "{autodesktop}\mei mei"; Filename: "{app}\mei mei.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\mei mei.exe"; Description: "Launch mei mei"; Flags: nowait postinstall skipifsilent

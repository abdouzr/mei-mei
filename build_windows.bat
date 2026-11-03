@echo off
pip install -r requirements.txt pyinstaller || exit /b 1
pyinstaller --noconfirm --windowed --name MeiMei mei_mei.py || exit /b 1
xcopy /E /I /Y images dist\MeiMei\images
copy /Y music.mp3 dist\MeiMei\
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer.iss
echo.
echo Done: installer\MeiMei-Setup.exe

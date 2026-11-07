@echo off
title Building HyperPulse Toolkit Standalone Executable...
echo ==============================================================
echo       HYPERPULSE TOOLKIT - PYINSTALLER COMPILER
echo ==============================================================
echo.
echo [1/3] Checking dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/3] Compiling standalone Windows .exe...
pyinstaller --noconfirm --onefile --windowed ^
    --name "HyperPulse-Toolkit" ^
    --add-data "bin;bin" ^
    --add-data "assets;assets" ^
    --add-data "version.json;." ^
    app.py

echo.
echo [3/3] Build completed!
echo.
echo The compiled standalone executable is: dist\HyperPulse-Toolkit.exe
echo You can run it directly or share it anywhere!
echo.
pause

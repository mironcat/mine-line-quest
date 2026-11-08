@echo off
rem Release build: dist\mine-line-quest.exe
cd /d "%~dp0"
python release.py %*
if errorlevel 1 (
  echo.
  echo Build failed.
  pause
  exit /b 1
)
pause

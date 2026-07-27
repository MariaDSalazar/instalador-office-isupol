@echo off
rem INSTITUTO SUPERIOR TECNOLOGICO POLICIA NACIONAL - Competencias Digitales
rem Lanzador: pide permisos de administrador y abre office-isupol.ps1
rem Los dos archivos deben estar en la MISMA carpeta.

chcp 65001 >nul
title ISUPOL - Instalador de Office
mode con: cols=100 lines=45

net session >nul 2>&1
if errorlevel 1 (
  powershell -NoProfile -Command "Start-Process '%~f0' -Verb RunAs"
  exit /b
)

if not exist "%~dp0office-isupol.ps1" (
  echo.
  echo  [!] Falta el archivo office-isupol.ps1 en esta misma carpeta.
  echo      Los dos archivos van juntos.
  echo.
  pause
  exit /b 1
)

rem Unblock-File quita la marca de "archivo bajado de internet",
rem que si no hace que PowerShell se niegue a ejecutarlo.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Unblock-File -LiteralPath '%~dp0office-isupol.ps1'; & '%~dp0office-isupol.ps1'"

if errorlevel 1 pause

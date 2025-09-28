@echo off
REM This batch file executes the PowerShell installer script, bypassing execution policy for this run only.
PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\install.ps1"
pause
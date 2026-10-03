@echo off
title Crimson Night: Vampire Survivors
cd /d "%~dp0"

REM Try user-installed Python first
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" main.py
    goto end
)

REM Fallback to standard python in PATH
python main.py

:end
if errorlevel 1 (
    echo.
    echo Game terminated with an error. Press any key to exit.
    pause >nul
)

@echo off
title Charging AI Agent Demo - Init

echo.
echo ============================================
echo   Charging AI Agent Demo - Environment Init
echo ============================================
echo.

if exist ".venv" (
    echo [INFO] Virtual environment already exists, skipping...
    goto install_deps
)

echo [1/2] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Python not found or not in PATH
    pause
    exit /b 1
)

echo [OK] Virtual environment created

:install_deps
echo.
echo [2/2] Installing dependencies...
call ".venv\Scripts\activate.bat"
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies, check network
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Initialization completed!
echo ============================================
echo.
echo   Run start.bat to launch the application
echo   Frontend: http://localhost:8501
echo ============================================
echo.
pause
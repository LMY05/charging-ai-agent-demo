@echo off
title Charging AI Agent Demo

echo.
echo ============================================
echo   Charging AI Agent Demo - Quick Start
echo ============================================
echo.

set "VENV_DIR=.venv"
set "BACKEND_PORT=8000"
set "FRONTEND_PORT=8501"

if not exist "%VENV_DIR%" (
    echo [ERROR] Virtual environment not found. Run init.bat first.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

echo.
echo [2/3] Starting backend service (FastAPI)...
start "Backend - FastAPI" cmd /k "cd /d %cd% && python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT%"

echo [3/3] Starting frontend service (Streamlit)...
start "Frontend - Streamlit" cmd /k "cd /d %cd% && streamlit run frontend/app.py --server.port %FRONTEND_PORT%"

echo.
echo ============================================
echo   Services started successfully!
echo ============================================
echo.
echo   Backend: http://localhost:%BACKEND_PORT%
echo   Frontend: http://localhost:%FRONTEND_PORT%
echo.
echo   Press any key to stop all services and exit...
echo ============================================
echo.

pause >nul

echo.
echo [CLEANUP] Stopping all services...

taskkill /F /FI "WINDOWTITLE eq Backend - FastAPI" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend - Streamlit" >nul 2>&1

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%BACKEND_PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%FRONTEND_PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [DONE] All services stopped!
echo.
pause
@echo off
chcp 65001 >nul
title Charging AI Agent Demo

echo.
echo ============================================
echo   Charging AI Agent Demo - 一键启动脚本
echo ============================================
echo.

set "VENV_DIR=.venv"
set "BACKEND_PORT=8000"
set "FRONTEND_PORT=8501"

if not exist "%VENV_DIR%" (
    echo [错误] 虚拟环境不存在，请先执行: python -m venv .venv
    pause
    exit /b 1
)

echo [1/3] 激活虚拟环境...
call "%VENV_DIR%\Scripts\activate.bat"

echo.
echo [2/3] 启动后端服务 (FastAPI)...
start "Backend - FastAPI" cmd /k "cd /d %cd% && python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT%"

echo [3/3] 启动前端服务 (Streamlit)...
start "Frontend - Streamlit" cmd /k "cd /d %cd% && streamlit run frontend/app.py --server.port %FRONTEND_PORT%"

echo.
echo ============================================
echo   服务启动完成！
echo ============================================
echo.
echo   后端地址: http://localhost:%BACKEND_PORT%
echo   前端地址: http://localhost:%FRONTEND_PORT%
echo.
echo   按任意键停止所有服务并退出...
echo ============================================
echo.

pause >nul

echo.
echo [清理] 停止所有服务...

taskkill /F /FI "WINDOWTITLE eq Backend - FastAPI" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend - Streamlit" >nul 2>&1

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%BACKEND_PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%FRONTEND_PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [完成] 所有服务已停止！
echo.
pause
@echo off
chcp 65001 >nul
title Charging AI Agent Demo - 初始化

echo.
echo ============================================
echo   Charging AI Agent Demo - 环境初始化
echo ============================================
echo.

if exist ".venv" (
    echo [提示] 虚拟环境已存在，跳过创建...
    goto install_deps
)

echo [1/2] 创建虚拟环境...
python -m venv .venv
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

echo [成功] 虚拟环境创建完成

:install_deps
echo.
echo [2/2] 安装依赖...
call ".venv\Scripts\activate.bat"
pip install -r requirements.txt

if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ============================================
echo   初始化完成！
echo ============================================
echo.
echo   现在可以运行 start.bat 启动服务
echo   前端地址: http://localhost:8501
echo ============================================
echo.
pause
@echo off
title 水仙花数查找器
echo 正在启动水仙花数查找器...

:: 检查是否安装了Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python安装
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b
)

:: 检查是否安装了streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo 检测到streamlit未安装，正在自动安装...
    pip install streamlit
)

:: 运行程序
echo 正在启动程序...
cd /d "%~dp0"
start "" streamlit run 水仙花数_streamlit.py

echo 程序已启动，请查看浏览器窗口...
pause

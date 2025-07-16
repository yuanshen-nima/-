@echo off
title 多功能计算器
echo 正在启动多功能计算器...

:: 检查Python环境
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python安装
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b
)

:: 检查streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo 检测到streamlit未安装，正在自动安装...
    pip install streamlit
)

:: 运行程序
echo 正在启动多功能计算器...
cd /d "%~dp0"
start "" streamlit run 多功能计算器.py

echo 程序已启动，请查看浏览器窗口...
echo 功能说明：
echo 1. 水仙花数查找器 - 查找指定位数的水仙花数
echo 2. 找零钱计算器 - 计算最优找零方案
pause

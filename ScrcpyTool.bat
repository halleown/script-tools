@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置scrcpy路径
set "SCRCPY_PATH=D:\Program\scrcpy-win64-v3.3.1"
:: 设置窗口宽高
set "W_WIDTH=800"
set "W_HEIGHT=500"

:menu
cls
echo ============================================
echo       SCRECPY 控制面板
echo ============================================
echo  当前配置路径: %SCRCPY_PATH%
echo --------------------------------------------
echo  1. 启动：正常模式
echo  2. 启动：熄灭手机屏幕 (保持唤醒)
echo  3. 调试：查看设备连接状态
echo  4. 退出
echo ============================================
set /p opt=请输入序号 (1-4): 

if "%opt%"=="1" goto start_normal
if "%opt%"=="2" goto start_off_screen
if "%opt%"=="3" goto list_devices
if "%opt%"=="4" exit
goto menu

:start_normal
echo [正在启动] 正常模式...
:: pushd 会自动处理盘符切换 (从 C: 切换到 D:)
pushd "%SCRCPY_PATH%"
scrcpy.exe --window-width %W_WIDTH% --window-height %W_HEIGHT%
if %errorlevel% neq 0 pause
popd
goto menu

:start_off_screen
echo [正在启动] 熄屏模式...
pushd "%SCRCPY_PATH%"
:: -S 熄屏，-w 保持唤醒
scrcpy.exe -S -w --window-width %W_WIDTH% --window-height %W_HEIGHT%
if %errorlevel% neq 0 pause
popd
goto menu

:list_devices
echo --------------------------------------------
pushd "%SCRCPY_PATH%"
adb.exe devices
popd
echo --------------------------------------------
pause
goto menu
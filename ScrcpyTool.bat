@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置scrcpy路径
set "SCRCPY_PATH=D:\Program\scrcpy-win64-v3.3.1"
:: 设置窗口宽高
set "W_WIDTH=800"
set "W_HEIGHT=500"

:: 初始化设备序列号变量
set "TARGET_DEVICE="

:menu
cls
echo ============================================
echo       SCRECPY 控制面板
echo ============================================
echo  当前配置路径: %SCRCPY_PATH%
if defined TARGET_DEVICE (
    echo  当前选中设备: %TARGET_DEVICE%
) else (
    echo  当前选中设备: [未选择 - 默认连接唯一设备]
)
echo --------------------------------------------
echo  1. 启动：正常模式
echo  2. 启动：熄灭手机屏幕 (保持唤醒)
echo  3. 调试：查看并选择指定设备
echo  4. 清除当前选择的设备
echo  5. 退出
echo ============================================
set /p opt=请输入序号 (1-5):

if "%opt%"=="1" goto start_normal
if "%opt%"=="2" goto start_off_screen
if "%opt%"=="3" goto select_device
if "%opt%"=="4" (set "TARGET_DEVICE=" & goto menu)
if "%opt%"=="5" exit
goto menu

:start_normal
echo [正在启动] 正常模式...
pushd "%SCRCPY_PATH%"
:: 动态添加 -s 参数
if defined TARGET_DEVICE (
    scrcpy.exe -s %TARGET_DEVICE% --window-width %W_WIDTH% --window-height %W_HEIGHT%
) else (
    scrcpy.exe --window-width %W_WIDTH% --window-height %W_HEIGHT%
)
if %errorlevel% neq 0 pause
popd
goto menu

:start_off_screen
echo [正在启动] 熄屏模式...
pushd "%SCRCPY_PATH%"
:: 动态添加 -s 参数
if defined TARGET_DEVICE (
    scrcpy.exe -s %TARGET_DEVICE% -S -w --window-width %W_WIDTH% --window-height %W_HEIGHT%
) else (
    scrcpy.exe -S -w --window-width %W_WIDTH% --window-height %W_HEIGHT%
)
if %errorlevel% neq 0 pause
popd
goto menu

:select_device
echo --------------------------------------------
echo 正在获取设备列表...
pushd "%SCRCPY_PATH%"

:: 自动解析 adb devices 结果并生成编号菜单
set count=0
for /f "tokens=1,2" %%i in ('adb.exe devices') do (
    if "%%j"=="device" (
        set /a count+=1
        set "dev_!count!=%%i"
        echo  [!count!] %%i
    )
)

if %count%==0 (
    echo [提示] 未检测到任何有效连接的设备。
    popd
    pause
    goto menu
)

echo --------------------------------------------
set /p dev_idx=请选择要绑定的设备编号 (1-%count%):

:: 验证输入有效性并赋值
if defined dev_!dev_idx! (
    for /f "delims=" %%a in ("dev_!dev_idx!") do set "TARGET_DEVICE=!%%a!"
    echo [成功] 已绑定设备: !TARGET_DEVICE!
) else (
    echo [错误] 输入序号无效。
)

popd
pause
goto menu
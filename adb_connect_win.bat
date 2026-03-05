@REM @echo off
chcp 65001
rem 设置adb命令的路径
set adb_path="D:\\Program_Files\\Android\\Sdk\\platform-tools\\adb.exe"

rem 设置设备的IP地址或者直接使用USB连接
set device_ip=192.166.5.118
set device_port=5555

rem 连接设备
%adb_path% connect %device_ip%:%device_port%

rem 等待一秒钟以确保连接成功
timeout /t 1

rem 检查连接是否成功
%adb_path% devices

rem 给予Root权限
%adb_path% -s %device_ip%:%device_port% root

rem 等待一秒钟以确保Root权限生效
timeout /t 0

rem 挂载文件系统为读写模式
%adb_path% -s %device_ip%:%device_port% remount  

rem 输出挂载状态
%adb_path% -s %device_ip%:%device_port% shell mount | find " / "

rem 等待2秒钟以确保输出可见
timeout /t 2

@REM rem 关闭窗口
@REM exit
pause
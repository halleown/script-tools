@echo off &PUSHD %~DP0 &TITLE Settings Tool

:menu
cls
echo Notes: Please connect device with adb, it's only adapter for Android 11.
echo === Menu ===
echo [1] view top activity
echo [2] view top fragment
echo [3] view activity stack
echo ============

:loop
set /p num=Please input a number:
if %num%==1 call :topActivity
if %num%==2 call :topFragment
if %num%==3 call :activityStack
if not %num%=="" goto loop

:topActivity
adb wait-for-device
adb shell "dumpsys activity top | grep ACTIVITY | tail -n 1"
echo.
goto :eof

:topFragment
adb wait-for-device
adb shell "dumpsys activity top | grep '#[0-9]: ' | tail -n 1"
echo.
goto :eof

:activityStack
adb wait-for-device
adb shell "dumpsys activity activities | grep '* ActivityRecord{'"
echo.
goto :eof
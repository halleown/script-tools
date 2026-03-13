@echo off
:: =============================================================
:: 脚本名称: FileCopyTool.bat
:: 功能描述: 从源目录复制文件到 目标根目录 下，生成一个12位纯数字的文件夹，复制并改名到此
:: 编写日期: 2026-03-13
:: 作者信息: halle
:: 版本号:   v1.0
:: 使用说明: 无
:: =============================================================
chcp 65001
setlocal enabledelayedexpansion

:: 目标根目录
set "target_path=E:\adb_logcat\target"
:: 源文件所在的具体目录
set "source_path=E:\adb_logcat\00123456789"
:: 指定生成的文件夹数量
set /a folder_count=10

:: --- 随机时间范围限制 ---
set /a min_year=2025
set /a max_year=2026
set /a min_month=1
set /a max_month=12

set /a year_diff=%max_year% - %min_year% + 1
set /a month_diff=%max_month% - %min_month% + 1

if not exist "%target_path%" mkdir "%target_path%"
if not exist "%source_path%" (
    echo [错误] 找不到源文件目录: "%source_path%"
    pause
    exit /b
)

echo 开始从 "%source_path%" 复制并生成 %folder_count% 个文件夹...
echo ------------------------------------------

for /l %%i in (1,1,%folder_count%) do (

    :: 生成 12 位纯数字随机文件夹名
    set "folder_name="
    for /l %%j in (1,1,3) do (
        set /a "r=!random!"
        set "folder_name=!folder_name!!r!"
    )
    set "folder_name=!folder_name:~0,12!"
    
    :: 定义当前循环的目标路径变量
    set "curr_full_dir=%target_path%\!folder_name!"
    set "curr_pdf_dir=!curr_full_dir!\pdf"

    :: 生成指定范围内的随机时间
    set /a "r_year=(!random! %% %year_diff%) + %min_year%"
    set /a "m_num=(!random! %% %month_diff%) + %min_month%"
    set /a "d_num=(!random! %% 28) + 1"
    set /a "h_num=!random! %% 24", "min_num=!random! %% 60", "sec_num=!random! %% 60"
    
    if !m_num! lss 10 (set "r_month=0!m_num!") else (set "r_month=!m_num!")
    if !d_num! lss 10 (set "r_day=0!d_num!") else (set "r_day=!d_num!")
    if !h_num! lss 10 (set "r_hour=0!h_num!") else (set "r_hour=!h_num!")
    if !min_num! lss 10 (set "r_min=0!min_num!") else (set "r_min=!min_num!")
    if !sec_num! lss 10 (set "r_sec=0!sec_num!") else (set "r_sec=!sec_num!")

    set "mydate=!r_year!-!r_month!-!r_day! !r_hour!-!r_min!-!r_sec!"

    :: 随机中文词组
    set "r_cn="
    set /a "cn_idx=!random! %% 4"
    set "list=防盗;UI测试;遥控测频;ECU克隆"
    set "n=0"
    for %%a in (!list!) do (
        if !n! equ !cn_idx! set "r_cn=(%%a)"
        set /a "n+=1"
    )

    :: 执行目录创建与文件复制
    echo [%%i/%folder_count%] 正在创建: !folder_name!
    
    if not exist "!curr_full_dir!" mkdir "!curr_full_dir!"
    if not exist "!curr_pdf_dir!" mkdir "!curr_pdf_dir!"

    :: 复制 PDF (去源目录下的 pdf 文件夹找)
    set "found_pdf=0"
    for %%f in ("%source_path%\pdf\*.pdf") do (
        if !found_pdf! equ 0 (
            copy /y "%%f" "!curr_pdf_dir!\!mydate!.pdf" >nul
            set "found_pdf=1"
        )
    )

    :: 复制 PNG (去源目录下的 pdf 文件夹找，最多 2 张)
    set /a p_count=0
    for %%f in ("%source_path%\pdf\*.png") do (
        if !p_count! lss 2 (
            copy /y "%%f" "!curr_pdf_dir!\!mydate!_!p_count!.png" >nul
            set /a p_count+=1
        )
    )

    :: 复制 JSON (去源目录根目录找)
    set "json_name=!r_cn!!r_year!_pingpai_!mydate!_0.json"
    set "found_json=0"
    for %%f in ("%source_path%\*.json") do (
        if !found_json! equ 0 (
            copy /y "%%f" "!curr_full_dir!\!json_name!" >nul
            set "found_json=1"
        )
    )
    echo [√] 已生成: !json_name!
)

echo ------------------------------------------
echo 任务完成！请检查 !target_path!
@REM pause
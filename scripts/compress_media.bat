@echo off
setlocal enabledelayedexpansion

:: Initialize counters
set "img_count=0"
set "video_count=0"
set "total_files=0"

:: Record start time (更兼容的时间获取方式)
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "start_datetime=%%a"
set "start_time=!start_datetime:~8,2!!start_datetime:~10,2!!start_datetime:~12,2!!start_datetime:~15,2!"

:: Define image extensions (小写，移除.gif)
set "img_exts=.jpg .jpeg .png .bmp .tiff .webp"
:: Define video extensions (小写)
set "video_exts=.mp4 .mkv .avi .flv .mov .wmv .m4v"

:: Recursively traverse files,屏蔽路径错误
for /r %%i in (*.*) do (
    :: 检查文件是否真实存在（跳过无效路径）
    if exist "%%~fi" (
        call :process_file "%%~fi"
    )
) 2>nul

:: Calculate total files
set /a "total_files=img_count+video_count"

:: Record end time
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "end_datetime=%%a"
set "end_time=!end_datetime:~8,2!!end_datetime:~10,2!!end_datetime:~12,2!!end_datetime:~15,2!"

:: Calculate duration (分钟:秒.毫秒)
set /a "duration=1!end_time! - 1!start_time!"
set /a "hours=duration/1000000, rem=duration%%1000000"
set /a "minutes=rem/10000, rem=rem%%10000"
set /a "seconds=rem/100, centiseconds=rem%%100"

:: Format numbers
if !hours! lss 10 set "hours=0!hours!"
if !minutes! lss 10 set "minutes=0!minutes!"
if !seconds! lss 10 set "seconds=0!seconds!"
if !centiseconds! lss 10 set "centiseconds=0!centiseconds!"

:: Print summary
echo.
echo ===================== SUMMARY =====================
echo Processed Images:  !img_count!
echo Processed Videos:  !video_count!
echo Total Files:       !total_files!
echo Total Time:        !hours!:!minutes!:!seconds!.!centiseconds!
echo ===================================================

endlocal
pause
goto :eof

:: File processing function
:process_file
set "fullpath=%~1"
set "filename=%~n1"
set "filepath=%~dp1"
set "extension=%~x1"

:: Skip temporary files
if /i "%~nx1"=="_temp.jpg" goto :eof
if /i "%~nx1"=="_temp.mp4" goto :eof

:: Check if it's an image file
echo !img_exts! | findstr /i /c:"!extension!" >nul 2>&1
if not errorlevel 1 (
    echo [Image Processing] !fullpath!
    set "tempfile=!filepath!!filename!_temp.jpg"
    
    ffmpeg -hide_banner -loglevel error -i "!fullpath!" -q:v 4 -y "!tempfile!" >nul 2>&1
    
    if exist "!tempfile!" (
        del /f /q "!fullpath!" >nul 2>&1
        ren "!tempfile!" "!filename!.jpg" >nul 2>&1
        set /a "img_count+=1"
    )
    goto :eof
)

:: Check if it's a video file
echo !video_exts! | findstr /i /c:"!extension!" >nul 2>&1
if not errorlevel 1 (
    echo [Video Processing] !fullpath!
    set "tempfile=!filepath!!filename!_temp.mp4"
    
    ffmpeg -hide_banner -loglevel error -i "!fullpath!" -c:v libx265 -crf 28 -tag:v hvc1 -c:a copy -map_metadata 0 -y "!tempfile!" >nul 2>&1
    
    if exist "!tempfile!" (
        del /f /q "!fullpath!" >nul 2>&1
        ren "!tempfile!" "!filename!.mp4" >nul 2>&1
        set /a "video_count+=1"
    )
    goto :eof
)

goto :eof

@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

net session >nul 2>&1
if errorlevel 1 (
    echo This script must be run as Administrator.
    echo.
    echo Right-click this file and choose:
    echo Run as administrator
    echo.
    pause
    exit /b 1
)

:menu
cls
echo Windows System Cleanup
echo.
echo 1. Run Disk Cleanup (cleanmgr)
echo 2. Analyze Component Store (DISM)
echo 3. Start Component Cleanup (DISM)
echo 4. Run 1 + 2 + 3
echo 5. Exit
echo.
set /p CHOICE=Choose an option [1-5]: 

if "%CHOICE%"=="1" goto cleanmgr
if "%CHOICE%"=="2" goto analyze
if "%CHOICE%"=="3" goto cleanup
if "%CHOICE%"=="4" goto all
if "%CHOICE%"=="5" goto end
goto menu

:cleanmgr
echo.
echo Opening Disk Cleanup...
cleanmgr
echo.
pause
goto menu

:analyze
echo.
echo Running:
echo DISM /Online /Cleanup-Image /AnalyzeComponentStore
echo.
DISM /Online /Cleanup-Image /AnalyzeComponentStore
echo.
pause
goto menu

:cleanup
echo.
echo Running:
echo DISM /Online /Cleanup-Image /StartComponentCleanup
echo.
DISM /Online /Cleanup-Image /StartComponentCleanup
echo.
pause
goto menu

:all
echo.
echo Step 1: Opening Disk Cleanup...
cleanmgr
echo.
echo Step 2: Running AnalyzeComponentStore...
DISM /Online /Cleanup-Image /AnalyzeComponentStore
echo.
echo Step 3: Running StartComponentCleanup...
DISM /Online /Cleanup-Image /StartComponentCleanup
echo.
pause
goto menu

:end
exit /b 0

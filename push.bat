@echo off
setlocal
echo ========================================================
echo   Surakshaa Saathi — Automatic GitHub Sync
echo ========================================================
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update Surakshaa Saathi platform

git add .
git commit -m "%commit_msg%"
git push origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS: Code pushed to GitHub repository!
    echo ========================================================
) else (
    echo.
    echo Git push failed, attempting fallback API sync...
    py github_sync.py "%commit_msg%"
)
echo.
pause
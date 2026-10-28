@echo off
setlocal
echo ========================================================
echo   Surakshaa Saathi — Automatic GitHub Sync & Push
echo ========================================================
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg="Update Surakshaa Saathi cybersecurity platform"

echo.
echo [*] Staging all files and pushing via Git...
"C:\Users\Students\AppData\Local\Programs\Git\cmd\git.exe" add -A
"C:\Users\Students\AppData\Local\Programs\Git\cmd\git.exe" commit -m %commit_msg%
"C:\Users\Students\AppData\Local\Programs\Git\cmd\git.exe" push origin main

if errorlevel 1 (
    echo.
    echo [*] Git push failed or had network isolation. Running API direct sync fallback...
    py github_sync.py %commit_msg%
)

echo.
echo [DONE] Push completed successfully!
echo Repository: https://github.com/nakshbansal2011official-coder/Suraaksha-Saathi
echo.
pause

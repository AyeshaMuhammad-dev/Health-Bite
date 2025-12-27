@echo off
echo.
echo ========================================
echo   Pushing Health-Bite to GitHub
echo ========================================
echo.
echo Your 5 commits are ready to push:
echo.
git log --oneline --date=short --pretty=format:"  %ad - %s" -5
echo.
echo.
echo Pushing to: https://github.com/AyeshaMuhammad-dev/Health-Bite.git
echo.
echo When prompted:
echo   Username: AyeshaMuhammad-dev
echo   Password: Use your Personal Access Token (NOT your GitHub password)
echo.
echo Get token: https://github.com/settings/tokens
echo.
echo ========================================
echo.
git push -u origin main --force
echo.
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo View your repository:
    echo https://github.com/AyeshaMuhammad-dev/Health-Bite
) else (
    echo.
    echo ========================================
    echo   PUSH FAILED
    echo ========================================
    echo.
    echo Possible issues:
    echo   1. Repository doesn't exist - Create it at: https://github.com/new
    echo   2. Need Personal Access Token - Get one at: https://github.com/settings/tokens
    echo   3. Wrong repository name or permissions
    echo.
)
echo.
pause

@echo off
echo ===================================
echo Git Upload Script for Expense Tracker
echo ===================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please download from: https://git-scm.com/download/win
    echo Or use GitHub Desktop: https://desktop.github.com
    pause
    exit /b 1
)

echo Step 1: Configuring Git...
echo Please enter your information:
echo.

set /p NAME="Enter your full name: "
set /p EMAIL="Enter your email (same as GitHub): "

git config --global user.name "%NAME%"
git config --global user.email "%EMAIL%"

echo.
echo Step 2: Initializing Git repository...
git init

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Creating initial commit...
git commit -m "Initial commit: Expense Tracker web application"

echo.
echo Step 5: Setting main branch...
git branch -M main

echo.
echo ===================================
echo Almost done! Follow these steps:
echo ===================================
echo.
echo 1. Go to your GitHub repository page
echo 2. Copy the repository URL (it looks like this):
echo    https://github.com/YOUR-USERNAME/expense-tracker.git
echo.
echo 3. Then run this command:
echo    git remote add origin YOUR-REPO-URL
echo    git push -u origin main
echo.
echo Example:
echo git remote add origin https://github.com/yourusername/expense-tracker.git
echo git push -u origin main
echo.
echo You'll be asked to login to GitHub - use your account
echo.
pause

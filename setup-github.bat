@echo off
echo 🚀 Setting up GitHub repository for StockAI...

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Please run this script from the stock-recommendation-website directory.
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Please run this script from the stock-recommendation-website directory.
    pause
    exit /b 1
)

REM Get GitHub username
set /p githubUsername="Enter your GitHub username: "
if "%githubUsername%"=="" (
    echo ❌ GitHub username is required.
    pause
    exit /b 1
)

REM Check git status
echo 📊 Checking git status...
git status

REM Add remote origin
echo 🔗 Adding GitHub remote...
git remote add origin https://github.com/%githubUsername%/stock-recommendation-website.git

REM Verify remote was added
echo ✅ Remote added. Verifying...
git remote -v

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🎯 Next steps:
    echo 1. Go to: https://github.com/%githubUsername%/stock-recommendation-website
    echo 2. Verify all files are uploaded correctly
    echo 3. Make sure the repository is PUBLIC
    echo 4. Follow the DEPLOYMENT.md guide for Vercel deployment
    echo.
    echo 🌐 Your repository URL: https://github.com/%githubUsername%/stock-recommendation-website
) else (
    echo ❌ Failed to push to GitHub. Please check the error above.
    echo 💡 Make sure you have created the repository on GitHub first.
)

pause

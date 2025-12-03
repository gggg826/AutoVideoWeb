@echo off
chcp 65001 >nul
title AdAlliance Tracker - Server Startup

echo ============================================================
echo    AdAlliance Tracker - Startup Script
echo ============================================================
echo.

:: Check Python installation
echo [1/5] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: Check virtual environment
echo [2/5] Checking virtual environment...
if not exist "backend\.venv\" (
    echo [INFO] Creating virtual environment...
    cd backend
    python -m venv .venv
    cd ..
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)
echo.

:: Activate virtual environment
echo [3/5] Activating virtual environment...
call backend\.venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

:: Check dependencies
echo [4/5] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install -r backend\requirements.txt

    :: Verify installation by trying to import again
    python -c "import fastapi" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
)
echo.

:: Check database
echo [5/5] Checking database...
if not exist "data\tracker.db" (
    echo [INFO] Initializing database...
    python backend\scripts\init_db.py
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize database
        pause
        exit /b 1
    )
    echo [OK] Database initialized
) else (
    echo [OK] Database exists
)
echo.

:: Start server
echo ============================================================
echo    Starting server...
echo ============================================================
echo.
echo Access URLs:
echo    - Home:      http://localhost:8000/
echo    - Test Page: http://localhost:8000/public/index.html
echo    - Admin:     http://localhost:8000/admin/index.html
echo    - API Docs:  http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

:: Start server
python run.py

:: If server exits with error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server exited abnormally
    pause
)

@echo off
REM Civic Image Classification API Deployment Script for Windows

echo 🚀 Starting Civic Image Classification API deployment...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements-api.txt

REM Check if model file exists
if not exist "best_model.h5" (
    echo ❌ Model file 'best_model.h5' not found. Please ensure the model is trained and saved.
    pause
    exit /b 1
)

REM Start the API
echo 🌟 Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API documentation will be available at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
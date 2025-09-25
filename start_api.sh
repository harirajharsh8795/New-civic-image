#!/bin/bash

# Civic Image Classification API Deployment Script

echo "🚀 Starting Civic Image Classification API deployment..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements-api.txt

# Check if model file exists
if [ ! -f "best_model.h5" ]; then
    echo "❌ Model file 'best_model.h5' not found. Please ensure the model is trained and saved."
    exit 1
fi

# Start the API
echo "🌟 Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API documentation will be available at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
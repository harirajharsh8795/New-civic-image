#!/usr/bin/env python3
"""
Railway startup script for Civic Image Classification API
"""
import os
import sys
import subprocess

def main():
    # Get port from environment or use default
    port = os.environ.get("PORT", "8000")
    
    print(f"🚂 Starting Railway deployment on port {port}")
    print(f"🐍 Python version: {sys.version}")
    
    # Check if model file exists
    if not os.path.exists("best_model.h5"):
        print("❌ Error: best_model.h5 not found!")
        sys.exit(1)
    
    model_size = os.path.getsize("best_model.h5") / (1024 * 1024)
    print(f"✅ Model found: best_model.h5 ({model_size:.1f} MB)")
    
    # Start the application
    try:
        cmd = [
            "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", str(port),
            "--workers", "1"
        ]
        
        print(f"🚀 Starting with command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("🛑 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
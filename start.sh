#!/bin/bash
# Railway Deployment Script

# Start the FastAPI application with Gunicorn
exec gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
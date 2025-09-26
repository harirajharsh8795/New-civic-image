# Railway-optimized Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal for Railway)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY best_model.h5 .

# Create non-root user
RUN useradd -m -u 1000 railwayuser && chown -R railwayuser:railwayuser /app
USER railwayuser

# Expose port (Railway will set PORT env var)
EXPOSE $PORT

# Command to run the application
CMD ["sh", "-c", "gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"]
# Civic Infrastructure Image Classification API

This FastAPI application provides an API for classifying civic infrastructure issues from images using a trained deep learning model.

## Features

- **Single Image Classification**: Upload and classify individual images
- **Batch Processing**: Process multiple images simultaneously
- **RESTful API**: Standard HTTP endpoints with JSON responses
- **Interactive Documentation**: Automatic API documentation with Swagger UI
- **Health Monitoring**: Health check endpoints for deployment monitoring
- **CORS Support**: Cross-origin resource sharing enabled
- **Docker Support**: Containerized deployment ready

## Supported Classifications

The model can identify the following civic infrastructure issues:

1. **garbage** - Cardboard and other garbage items
2. **open_manhole** - Open manholes on roads
3. **potholes** - Road potholes
4. **road_normal** - Normal road conditions
5. **streetlight bad** - Damaged/broken streetlights
6. **streetlight good** - Working streetlights

## Quick Start

### Method 1: Using the Startup Script (Recommended)

**Windows:**
```bash
.\start_api.bat
```

**Linux/Mac:**
```bash
chmod +x start_api.sh
./start_api.sh
```

### Method 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements-api.txt
   ```

2. **Start the API:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API:**
   - API Base URL: http://localhost:8000
   - Interactive Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /classes` - Get all available classification categories

### Prediction Endpoints

- `POST /predict` - Classify a single image
- `POST /batch-predict` - Classify multiple images (max 10)

### Example Usage

#### Single Image Prediction
```python
import requests

# Upload and classify an image
with open('your_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/predict', files=files)
    result = response.json()
    
print(f"Predicted: {result['predicted_class']}")
print(f"Confidence: {result['confidence']}")
```

#### Using cURL
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

## Docker Deployment

### Build and Run with Docker
```bash
# Build the image
docker build -t civic-image-api .

# Run the container
docker run -p 8000:8000 civic-image-api
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

Make sure the API server is running before executing tests.

## API Response Format

### Single Prediction Response
```json
{
  "predicted_class": "potholes",
  "confidence": 0.9234,
  "all_predictions": {
    "garbage": 0.0123,
    "open_manhole": 0.0098,
    "potholes": 0.9234,
    "road_normal": 0.0234,
    "streetlight bad": 0.0156,
    "streetlight good": 0.0155
  },
  "image_info": {
    "filename": "test_image.jpg",
    "size": 245760,
    "content_type": "image/jpeg"
  }
}
```

### Batch Prediction Response
```json
{
  "results": [
    {
      "filename": "image1.jpg",
      "predicted_class": "potholes",
      "confidence": 0.9234,
      "all_predictions": {...}
    },
    {
      "filename": "image2.jpg",
      "predicted_class": "garbage",
      "confidence": 0.8567,
      "all_predictions": {...}
    }
  ]
}
```

## Production Deployment

### Environment Variables
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of worker processes
- `LOG_LEVEL`: Logging level (info, debug, warning, error)

### Performance Considerations
- Use multiple workers for production: `uvicorn main:app --workers 4`
- Consider using a reverse proxy (nginx) for production
- Implement rate limiting for public APIs
- Monitor memory usage with large models

### Security
- Configure CORS origins properly for production
- Add authentication if needed
- Use HTTPS in production
- Validate file types and sizes
- Implement request rate limiting

## Troubleshooting

### Common Issues

1. **Model not found error:**
   - Ensure `best_model.h5` exists in the project directory
   - Check if the model was trained and saved correctly

2. **Memory issues:**
   - Reduce batch size for batch predictions
   - Consider using model quantization for deployment

3. **Dependency issues:**
   - Use the provided `requirements-api.txt`
   - Ensure compatible TensorFlow version

4. **Port conflicts:**
   - Change the port using `--port` parameter
   - Check if port 8000 is already in use

### Logs
Monitor logs for debugging:
```bash
# Local development
uvicorn main:app --log-level debug

# Docker
docker-compose logs -f civic-image-api
```

## Development

### Adding New Features
1. Modify `main.py` for new endpoints
2. Update tests in `test_api.py`
3. Update documentation

### Model Updates
1. Replace `best_model.h5` with new model
2. Update `class_names` list if categories change
3. Restart the API service

## License

This project is part of the civic infrastructure monitoring system.
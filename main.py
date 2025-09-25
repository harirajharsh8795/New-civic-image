from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Civic Infrastructure Image Classification API",
    description="API for classifying civic infrastructure issues from images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
class_names = ['garbage', 'open_manhole', 'potholes', 'road_normal', 'streetlight bad', 'streetlight good']
IMG_SIZE = 224

def load_model():
    """Load the trained model"""
    global model
    try:
        model = tf.keras.models.load_model('best_model.h5')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for prediction"""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize((IMG_SIZE, IMG_SIZE))
        
        # Convert to numpy array and normalize
        img_array = np.array(image)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise e

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Civic Infrastructure Image Classification API",
        "status": "running",
        "model_loaded": model is not None,
        "classes": class_names
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict civic infrastructure issue from uploaded image
    
    Returns:
        - predicted_class: The predicted class name
        - confidence: Confidence score for the prediction
        - all_predictions: Confidence scores for all classes
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Create response
        response = {
            "predicted_class": class_names[predicted_class_idx],
            "confidence": confidence,
            "all_predictions": {
                class_names[i]: float(predictions[0][i]) 
                for i in range(len(class_names))
            },
            "image_info": {
                "filename": file.filename,
                "size": len(contents),
                "content_type": file.content_type
            }
        }
        
        logger.info(f"Prediction made: {class_names[predicted_class_idx]} with confidence {confidence:.4f}")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/batch-predict")
async def batch_predict(files: list[UploadFile] = File(...)):
    """
    Predict civic infrastructure issues from multiple uploaded images
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed per batch")
    
    results = []
    
    for file in files:
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "error": "File must be an image"
            })
            continue
        
        try:
            # Process each image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            processed_image = preprocess_image(image)
            
            # Make prediction
            predictions = model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            results.append({
                "filename": file.filename,
                "predicted_class": class_names[predicted_class_idx],
                "confidence": confidence,
                "all_predictions": {
                    class_names[i]: float(predictions[0][i]) 
                    for i in range(len(class_names))
                }
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": f"Error processing image: {str(e)}"
            })
    
    return JSONResponse(content={"results": results})

@app.get("/classes")
async def get_classes():
    """Get all available classes"""
    return {
        "classes": class_names,
        "total_classes": len(class_names),
        "descriptions": {
            "garbage": "Cardboard and other garbage items",
            "open_manhole": "Open manholes on roads",
            "potholes": "Road potholes",
            "road_normal": "Normal road conditions",
            "streetlight bad": "Damaged/broken streetlights",
            "streetlight good": "Working streetlights"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
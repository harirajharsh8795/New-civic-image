import requests
import json
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_classes():
    """Test classes endpoint"""
    print("Testing classes endpoint...")
    response = requests.get(f"{API_URL}/classes")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_prediction(image_path):
    """Test single image prediction"""
    print(f"Testing prediction with {image_path}...")
    
    if not Path(image_path).exists():
        print(f"Image file {image_path} not found!")
        return
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted Class: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"All Predictions: {json.dumps(result['all_predictions'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_batch_prediction(image_paths):
    """Test batch prediction"""
    print("Testing batch prediction...")
    
    files = []
    for path in image_paths:
        if Path(path).exists():
            files.append(('files', open(path, 'rb')))
        else:
            print(f"Warning: {path} not found, skipping...")
    
    if not files:
        print("No valid image files found!")
        return
    
    try:
        response = requests.post(f"{API_URL}/batch-predict", files=files)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()['results']
            for result in results:
                if 'error' in result:
                    print(f"Error for {result['filename']}: {result['error']}")
                else:
                    print(f"File: {result['filename']}")
                    print(f"  Predicted: {result['predicted_class']}")
                    print(f"  Confidence: {result['confidence']:.4f}")
        else:
            print(f"Error: {response.text}")
    finally:
        # Close all file handles
        for _, file_handle in files:
            file_handle.close()
    
    print("-" * 50)

if __name__ == "__main__":
    print("🧪 Testing Civic Image Classification API")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        test_health()
        test_classes()
        
        # Test single prediction with sample images
        sample_images = [
            "images/garbage.jpg",
            "images/pothole_imgae.jpg",
            "images/open manhole.jpg",
            "images/good streetlight.jpg"
        ]
        
        for img_path in sample_images:
            test_prediction(img_path)
        
        # Test batch prediction
        available_images = [img for img in sample_images if Path(img).exists()]
        if available_images:
            test_batch_prediction(available_images[:2])  # Test with first 2 available images
        
        print("✅ API testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
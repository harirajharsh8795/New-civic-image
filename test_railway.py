import requests
import json
import sys

def test_railway_deployment(base_url):
    """Test deployed API on Railway"""
    
    print(f"🧪 Testing Railway Deployment: {base_url}")
    print("=" * 60)
    
    try:
        # Test health endpoint
        print("1. Testing Health Endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=30)
        print(f"   Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"   Response: {health_response.json()}")
            print("   ✅ Health check passed!")
        else:
            print("   ❌ Health check failed!")
            return False
        
        print("-" * 40)
        
        # Test root endpoint
        print("2. Testing Root Endpoint...")
        root_response = requests.get(f"{base_url}/", timeout=30)
        print(f"   Status: {root_response.status_code}")
        if root_response.status_code == 200:
            data = root_response.json()
            print(f"   API Status: {data.get('status')}")
            print(f"   Model Loaded: {data.get('model_loaded')}")
            print(f"   Deployed On: {data.get('deployed_on')}")
            print("   ✅ Root endpoint working!")
        else:
            print("   ❌ Root endpoint failed!")
        
        print("-" * 40)
        
        # Test classes endpoint
        print("3. Testing Classes Endpoint...")
        classes_response = requests.get(f"{base_url}/classes", timeout=30)
        print(f"   Status: {classes_response.status_code}")
        if classes_response.status_code == 200:
            classes_data = classes_response.json()
            print(f"   Available Classes: {len(classes_data['classes'])}")
            for class_name in classes_data['classes']:
                print(f"     - {class_name}")
            print("   ✅ Classes endpoint working!")
        else:
            print("   ❌ Classes endpoint failed!")
        
        print("-" * 40)
        print("🎉 Basic API tests completed successfully!")
        print("\n📚 API Documentation available at:")
        print(f"   {base_url}/docs")
        print(f"   {base_url}/redoc")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check if the Railway deployment is complete")
        print("2. Verify the URL is correct")
        print("3. Wait a few minutes for the service to start")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    print("🚂 Railway Deployment Tester")
    print("="*40)
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = input("Enter your Railway app URL (e.g., https://your-app.up.railway.app): ").strip().rstrip('/')
    
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    success = test_railway_deployment(base_url)
    
    if success:
        print("\n✅ Your API is successfully deployed on Railway!")
        print("\n🔗 Share your API:")
        print(f"   Public URL: {base_url}")
        print(f"   Documentation: {base_url}/docs")
    else:
        print("\n❌ Deployment test failed. Check the troubleshooting guide.")

if __name__ == "__main__":
    main()
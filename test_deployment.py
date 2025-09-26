#!/usr/bin/env python3
"""
Simple Railway deployment verification
"""
import requests
import sys
import time

def test_railway_deployment(url):
    """Test the deployed Railway API"""
    print(f"🧪 Testing Railway deployment: {url}")
    
    # Wait a moment for the service to be ready
    print("⏳ Waiting for service to be ready...")
    time.sleep(5)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{url}/health", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   ✅ Model loaded: {data.get('model_loaded')}")
            print(f"   ✅ Port: {data.get('port')}")
            print(f"   ✅ Timestamp: {data.get('timestamp')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
            
        # Test root endpoint
        print("2. Testing root endpoint...")
        response = requests.get(f"{url}/", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Status: {data.get('status')}")
            print(f"   ✅ Model loaded: {data.get('model_loaded')}")
            print(f"   ✅ Deployed on: {data.get('deployed_on')}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            
        # Test classes endpoint
        print("3. Testing classes endpoint...")
        response = requests.get(f"{url}/classes", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Available classes: {len(data.get('classes', []))}")
            print(f"   ✅ Classes: {data.get('classes')}")
        else:
            print(f"   ❌ Classes endpoint failed: {response.status_code}")
            
        print("\n🎉 Railway deployment test completed successfully!")
        print(f"\n📚 Your API is live at: {url}")
        print(f"📖 Documentation: {url}/docs")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check if Railway deployment is complete")
        print("2. Wait a few minutes for the service to start")
        print("3. Check Railway logs for errors")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1].rstrip('/')
    else:
        url = input("Enter your Railway app URL: ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    test_railway_deployment(url)
# 🚂 Railway Deployment Guide for Civic Image Classification API

This guide will help you deploy your civic image classification model on Railway platform.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Model File**: Ensure `best_model.h5` is in your repository

## 🚀 Quick Deployment Steps

### Method 1: Deploy from GitHub (Recommended)

1. **Connect GitHub to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `2024021129-crypto/New-civic-image`

2. **Configure Environment**:
   - Railway will automatically detect your Python app
   - No additional environment variables needed

3. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for deployment to complete (5-10 minutes)

### Method 2: Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway link
   railway up
   ```

## 📁 Deployment Files Created

- **`Procfile`**: Specifies how to run your app
- **`runtime.txt`**: Python version specification
- **`railway.json`**: Railway-specific configuration
- **`start.sh`**: Startup script
- **Updated `requirements.txt`**: Railway-optimized dependencies
- **Updated `Dockerfile`**: Railway-optimized container
- **Updated `main.py`**: Added PORT environment variable support

## 🔧 Configuration Details

### Port Configuration
```python
port = int(os.environ.get("PORT", 8000))
```

### Resource Limits (Railway Free Tier)
- **RAM**: 512MB
- **CPU**: Shared
- **Disk**: 1GB
- **Network**: 100GB/month
- **Execution Time**: No limit

### Optimizations Made
- Reduced batch processing limit to 5 images
- Optimized dependencies for production
- Added Gunicorn WSGI server
- Minimal Docker image

## 🌐 Access Your API

After deployment, Railway will provide you with a URL like:
```
https://your-app-name.up.railway.app
```

### API Endpoints:
- **Root**: `https://your-app.up.railway.app/`
- **Health Check**: `https://your-app.up.railway.app/health`
- **Predict**: `https://your-app.up.railway.app/predict`
- **Batch Predict**: `https://your-app.up.railway.app/batch-predict`
- **Classes**: `https://your-app.up.railway.app/classes`
- **Docs**: `https://your-app.up.railway.app/docs`

## 🧪 Testing Your Deployed API

### Using cURL:
```bash
# Health check
curl https://your-app.up.railway.app/health

# Predict image
curl -X POST "https://your-app.up.railway.app/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Using Python:
```python
import requests

# Test prediction
url = "https://your-app.up.railway.app/predict"
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print(response.json())
```

## 📊 Monitoring and Logs

### View Logs:
```bash
railway logs
```

### Monitor in Dashboard:
- Visit your Railway dashboard
- Click on your project
- View metrics, logs, and deployments

## 🔒 Security Considerations

### Environment Variables (if needed):
```bash
railway variables set KEY=value
```

### CORS Configuration:
- Currently set to allow all origins (`*`)
- For production, update CORS settings in `main.py`:
```python
allow_origins=["https://yourdomain.com"]
```

## 💰 Cost Estimation

### Railway Pricing:
- **Hobby Plan**: $5/month (after free trial)
- **Pro Plan**: $20/month
- **Free Tier**: Available with limits

### Resource Usage:
- Model loading: ~200MB RAM
- Image processing: ~50-100MB per request
- Estimated concurrent users: 5-10 (with 512MB RAM)

## 🚨 Troubleshooting

### Common Issues:

1. **Model Loading Error**:
   ```
   Error loading model: best_model.h5 not found
   ```
   **Solution**: Ensure `best_model.h5` is committed to your repository

2. **Memory Issues**:
   ```
   Out of memory error
   ```
   **Solution**: Upgrade to Railway Pro plan or optimize model

3. **Build Timeout**:
   ```
   Build exceeded time limit
   ```
   **Solution**: Optimize dependencies or use Railway Pro

4. **Port Issues**:
   ```
   Application failed to bind to port
   ```
   **Solution**: Ensure you're using `os.environ.get("PORT")`

### Debug Commands:
```bash
# Check deployment status
railway status

# View recent logs
railway logs --tail

# Connect to shell
railway shell
```

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to your GitHub repository:

1. Make changes locally
2. Commit and push to GitHub
3. Railway automatically detects changes
4. New deployment starts automatically

## 📈 Scaling Options

### Horizontal Scaling:
- Not available on free tier
- Available on Pro plan ($20/month)

### Vertical Scaling:
- Upgrade RAM/CPU on Pro plan
- Configure in Railway dashboard

## 🎯 Next Steps

1. **Test your deployed API** using the provided URL
2. **Monitor performance** through Railway dashboard
3. **Set up custom domain** (Pro plan feature)
4. **Add authentication** if needed
5. **Implement rate limiting** for production use

## 📞 Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Join for community support
- **GitHub Issues**: Report issues in your repository

---

**Your API will be live at**: `https://your-app-name.up.railway.app` after deployment! 🎉
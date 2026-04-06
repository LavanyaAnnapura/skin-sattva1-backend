# Skin Sattva Backend - Deployment Guide

## 🚀 Deploy to Render

### Prerequisites
- GitHub repository with your backend code
- Render account (free at render.com)

### Step 1: Connect Your Repository
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file

### Step 2: Configure Services
Render will automatically create:
- **Web Service**: Your FastAPI backend
- **PostgreSQL Database**: Managed database

### Step 3: Set Environment Variables
In your Render dashboard, go to your web service and add:

**Required:**
- `GOOGLE_SHEETS_WEBHOOK_URL` - Your Google Sheets webhook URL (if using)

**Optional:**
- Any other environment variables your app needs

**Note:** `DATABASE_URL` and `PORT` are automatically provided by Render.

### Step 4: Deploy
1. Click "Create Blueprint"
2. Wait for the build and deployment to complete
3. Your API will be available at: `https://your-service-name.onrender.com`

### Step 5: Test Your API
```bash
# Test the API
curl https://your-service-name.onrender.com/api/bookings

# Create a booking
curl -X POST https://your-service-name.onrender.com/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "phone": "+1234567890",
    "service": "Consultation",
    "preferred_date": "2024-01-15",
    "preferred_time": "10:00 AM",
    "message": "Test booking"
  }'
```

## 📊 API Endpoints

- `POST /api/bookings` - Create a new booking
- `GET /api/bookings` - Get all bookings
- `GET /docs` - FastAPI interactive documentation

## 🔧 Troubleshooting

### Database Connection Issues
- Check that the PostgreSQL service is running
- Verify `DATABASE_URL` is set correctly
- Run migrations manually if needed

### Build Failures
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### Runtime Errors
- Check application logs in Render dashboard
- Test locally with the same environment variables
- Verify Google Sheets webhook URL if using integration

## 💰 Pricing

- **Free Tier**: 750 hours/month, sleeps after 15min inactivity
- **Paid Plans**: From $7/month for always-on service

## 🔄 Updates

Push changes to your Git repository - Render will automatically redeploy!

---

**Need help?** Check the [Render FastAPI docs](https://docs.render.com/deploy-fastapi) or [FastAPI deployment guide](https://fastapi.tiangolo.com/deployment/).
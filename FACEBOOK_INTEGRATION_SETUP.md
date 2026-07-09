# Facebook OAuth Integration Setup Guide

This guide will help you set up Facebook OAuth login and auto-posting functionality for your social media platform.

## 📋 Prerequisites

- A Facebook Developer Account
- Your Django backend running on `http://localhost:8000`
- Your frontend running on `http://localhost:5173` (or your Vite port)

## 🔧 Step 1: Create Facebook App

1. Go to [Facebook Developers Portal](https://developers.facebook.com/)
2. Click "My Apps" → "Create App"
3. Choose "Consumer" as app type
4. Fill in your app details:
   - App Name: Your Social Media Platform
   - Contact Email: Your email
   - Click "Create App"

## ⚙️ Step 2: Configure Facebook App Settings

### 2.1 Add Facebook Login Product

1. In your app dashboard, click "Add Product"
2. Find "Facebook Login" and click "Set Up"
3. Choose "Web" as platform
4. Enter your site URL: `http://localhost:5173`

### 2.2 Configure OAuth Settings

1. Go to "Facebook Login" → "Settings"
2. Set **Valid OAuth Redirect URIs**:
   ```
   http://localhost:8000/api/social-accounts/facebook/callback/
   ```
3. Enable "Client OAuth Login": Yes
4. Enable "Web OAuth Login": Yes
5. Enable "Use Strict Mode for Redirect URIs": Yes (recommended for production)

### 2.3 Get App Credentials

1. Go to "Settings" → "Basic"
2. Copy your **App ID** and **App Secret**
3. Keep these secure!

## 🔐 Step 3: Configure Your Backend

### 3.1 Update Settings

Open `backend/config/settings.py` and replace the placeholder values:

```python
# Facebook OAuth Configuration
FACEBOOK_APP_ID = "YOUR_ACTUAL_APP_ID_HERE"
FACEBOOK_APP_SECRET = "YOUR_ACTUAL_APP_SECRET_HERE"
FACEBOOK_REDIRECT_URI = "http://localhost:8000/api/social-accounts/facebook/callback/"
FACEBOOK_GRAPH_API_VERSION = "v18.0"
```

### 3.2 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3.3 Run Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 3.4 Start Backend Server

```bash
cd backend
python manage.py runserver
```

## 🎨 Step 4: Configure Your Frontend

### 4.1 Update Facebook App ID

Open `frontend/src/pages/Posts.jsx` and replace the placeholder:

```javascript
const FACEBOOK_APP_ID = "YOUR_ACTUAL_APP_ID_HERE";
```

### 4.2 Start Frontend Server

```bash
cd frontend
npm install
npm run dev
```

## 🚀 Step 5: Test the Integration

### 5.1 Login Flow

1. Open your application in browser: `http://localhost:5173`
2. Login with your regular credentials
3. Navigate to the Posts page
4. Click the "FB" button next to "Create Post"
5. A popup will open with Facebook login
6. Enter your Facebook credentials
7. Authorize the app permissions
8. You'll be redirected back and the popup will close
9. The Facebook connection status will update

### 5.2 Share Post to Facebook

1. Create a new post in your application
2. Click the "📘 Share" button on any post
3. The post will be published to your Facebook timeline
4. You'll see a success message

## 📱 Features Implemented

### Backend Features

1. **Facebook OAuth Login**
   - `/api/social-accounts/facebook/login/` - Get Facebook login URL
   - `/api/social-accounts/facebook/callback/` - Handle OAuth callback
   - `/api/social-accounts/facebook/status/` - Check connection status

2. **Facebook Post Sharing**
   - `/api/social-accounts/facebook/share/<post_id>/` - Share post to Facebook
   - Supports text posts and image posts
   - Automatically updates post status to "published"

3. **Social Account Management**
   - Stores Facebook access tokens securely
   - Tracks connection status
   - Manages multiple social accounts per user

### Frontend Features

1. **Facebook Login Button**
   - Opens Facebook OAuth in a popup
   - Automatically detects when user completes login
   - Updates connection status in real-time

2. **Share to Facebook Button**
   - Appears on each post when Facebook is connected
   - One-click sharing to Facebook
   - Shows success/error messages

3. **Connection Status**
   - Shows Facebook connection state
   - Hides login button when connected
   - Shows share buttons when connected

## 🔒 Security Considerations

1. **Never commit credentials** to version control
2. Use environment variables in production:
   ```python
   # In settings.py
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
   FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
   ```

3. Store access tokens encrypted in production
4. Use HTTPS in production (required by Facebook)
5. Implement token refresh logic for long-lived tokens

## 🐛 Troubleshooting

### Issue: "Invalid OAuth redirect URI"
**Solution**: Ensure the redirect URI in Facebook App settings exactly matches:
```
http://localhost:8000/api/social-accounts/facebook/callback/
```

### Issue: "Access token expired"
**Solution**: Facebook access tokens expire. Implement token refresh:
```python
# Extend token validity
url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/oauth/access_token"
params = {
    'grant_type': 'fb_exchange_token',
    'client_id': settings.FACEBOOK_APP_ID,
    'client_secret': settings.FACEBOOK_APP_SECRET,
    'fb_exchange_token': short_lived_token,
}
```

### Issue: "Permission denied"
**Solution**: Ensure you've requested the correct permissions in the scope:
```python
scope = "pages_show_list,pages_read_engagement,pages_manage_posts,public_profile,email"
```

### Issue: Popup blocked
**Solution**: Ensure the Facebook login is triggered by a user action (button click), not automatically.

## 📚 API Endpoints Reference

### Backend Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/social-accounts/facebook/login/` | GET | Get Facebook OAuth URL | Required |
| `/api/social-accounts/facebook/callback/` | GET | OAuth callback handler | Not required |
| `/api/social-accounts/facebook/status/` | GET | Check connection status | Required |
| `/api/social-accounts/facebook/share/<post_id>/` | POST | Share post to Facebook | Required |

### Request/Response Examples

#### Get Facebook Login URL
```javascript
GET /api/social-accounts/facebook/login/
Authorization: Bearer <access_token>

Response:
{
  "login_url": "https://www.facebook.com/v18.0/dialog/oauth?client_id=..."
}
```

#### Check Facebook Status
```javascript
GET /api/social-accounts/facebook/status/
Authorization: Bearer <access_token>

Response (connected):
{
  "is_connected": true,
  "account_name": "John Doe",
  "account_id": "123456789"
}

Response (not connected):
{
  "is_connected": false
}
```

#### Share Post to Facebook
```javascript
POST /api/social-accounts/facebook/share/1/
Authorization: Bearer <access_token>

Response (success):
{
  "message": "Post shared to Facebook successfully",
  "facebook_post_id": "123456789_987654321",
  "post_id": 1
}

Response (error):
{
  "error": "Failed to share post to Facebook",
  "details": {...}
}
```

## 🎯 Next Steps

1. **Add more social platforms**: Extend the pattern to support Instagram, Twitter, LinkedIn
2. **Implement scheduled posting**: Use the existing scheduler app to post at specific times
3. **Add analytics**: Track post performance on Facebook
4. **Implement webhooks**: Receive real-time updates from Facebook
5. **Add image optimization**: Compress images before uploading to Facebook
6. **Implement error retry**: Automatically retry failed posts
7. **Add post preview**: Show how the post will look on Facebook

## 📖 Additional Resources

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login/)
- [Facebook Sharing Documentation](https://developers.facebook.com/docs/sharing/)
- [Facebook SDK for Python](https://facebook-sdk.readthedocs.io/)

## ⚠️ Important Notes

1. **Facebook App Review**: For production, you'll need to submit your app for Facebook review to get approved for the requested permissions
2. **Rate Limits**: Facebook has rate limits on API calls. Implement proper error handling
3. **Token Expiration**: Access tokens expire. Implement token refresh logic
4. **Privacy Policy**: You must have a privacy policy URL in your Facebook app settings
5. **Terms of Service**: Ensure compliance with Facebook's Platform Terms

## 🆘 Support

If you encounter issues:
1. Check the browser console for frontend errors
2. Check the Django logs for backend errors
3. Verify Facebook App settings
4. Ensure all URLs are correctly configured
5. Test with Facebook's [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
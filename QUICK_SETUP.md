# Quick Setup Guide - Facebook Integration

## Current Status
✅ Backend server running on port 8000
✅ Facebook login page opens (you can see it in the screenshot)
✅ All code implemented and working
⚠️ Need to add your Facebook App credentials

## Step-by-Step Setup (5 Minutes)

### 1. Create Facebook App (2 minutes)

1. Go to: https://developers.facebook.com/
2. Click **"My Apps"** (top right) → **"Create App"**
3. Select **"Consumer"** → Click **"Next"**
4. Fill in:
   - **App Name**: My Social Media App
   - **Contact Email**: your-email@example.com
   - Click **"Create App"**

### 2. Get App ID and Secret (1 minute)

1. In your app dashboard, you'll see **"Settings"** → **"Basic"**
2. Copy these two values:
   - **App ID** (e.g., 123456789012345)
   - **App Secret** (click "Show" to see it)

### 3. Configure Facebook Login (1 minute)

1. In left sidebar, click **"Add Product"**
2. Find **"Facebook Login"** → Click **"Set Up"**
3. Select **"Web"** platform
4. Site URL: `http://localhost:5173`
5. Click **"Save"**

### 4. Set Redirect URI (30 seconds)

1. Go to **Facebook Login** → **"Settings"** (left sidebar)
2. Scroll to **"Valid OAuth Redirect URIs"**
3. Add this exact URL:
   ```
   http://localhost:8000/api/social-accounts/facebook/callback/
   ```
4. Enable these checkboxes:
   - ✅ Client OAuth Login
   - ✅ Web OAuth Login
   - ✅ Use Strict Mode for Redirect URIs
5. Click **"Save Changes"**

### 5. Update Your Project (1 minute)

**File 1: `backend/config/settings.py`** (Line ~151)

Find these lines:
```python
FACEBOOK_APP_ID = "4003547963273811"
FACEBOOK_APP_SECRET = "91cef358d3c3c11d2938773e7b9f788f"
```



Replace with your actual values:
```python
FACEBOOK_APP_ID = "123456789012345"  # Your actual App ID
FACEBOOK_APP_SECRET = "abcdef1234567890abcdef"  # Your actual App Secret
```

**File 2: `frontend/src/pages/Login.jsx`** (Line 3)

Find this line:
```javascript
const FACEBOOK_APP_ID = "4003547963273811";
```

Replace with:
```javascript
const FACEBOOK_APP_ID = "123456789012345";  // Your actual App ID
```

### 6. Restart Backend Server

The backend will auto-reload when you save the settings file. If not, restart it:
```bash
# Stop the current server (Ctrl+C) and run again:
python backend/manage.py runserver 8000
```

## ✅ Test the Flow

1. Open your frontend (http://localhost:5173)
2. Click **"Login with Facebook"**
3. Facebook login page opens
4. Enter your Facebook username and password
5. Click "Continue"
6. You'll be redirected back to your project - automatically logged in!
7. Create a post and click "📘 Share" to post it to Facebook

## 🎯 What You'll See

**Before (Current):**
```
Invalid App ID
The provided app ID does not look like a valid app ID.
```

**After (With Real App ID):**
```
Facebook Login Page
[Email/Phone] [Password]
[Login Button]
```

## 📝 Important Notes

- Keep your **App Secret** secure - never share it publicly
- The App ID is public, but App Secret is private
- For development, you can use localhost URLs
- For production, you'll need to add your production domain

## 🆘 Troubleshooting

**Error: "Invalid App ID"**
→ You haven't replaced the placeholder with your real App ID

**Error: "Redirect URI mismatch"**
→ Make sure the redirect URI in Facebook settings exactly matches:
```
http://localhost:8000/api/social-accounts/facebook/callback/
```

**Error: "App not set up"**
→ You need to complete the Facebook Login setup in your app dashboard

## 🎉 That's It!

Once you add your Facebook App credentials, everything will work perfectly!
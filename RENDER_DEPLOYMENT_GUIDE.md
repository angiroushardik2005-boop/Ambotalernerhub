# 🚀 Complete Render.com Deployment Guide - Ambota Learners Hub

## 📋 What You'll Get

- ✅ **Free PostgreSQL Database** (1GB)
- ✅ **Automatic HTTPS/SSL**
- ✅ **Git-based auto-deployment**
- ✅ **750 hours/month** (enough for 24/7 operation for one app)
- ✅ **100GB bandwidth**
- ✅ **Better performance** than PythonAnywhere
- ⚠️ **App sleeps after 15 min inactivity** (wakes up in 30-50 seconds)

---

## 🎯 Prerequisites

### 1. **GitHub Account** (Required)
- Create account at: https://github.com
- Render deploys directly from GitHub

### 2. **Your Project Ready**
- ✅ All files extracted from ZIP
- ✅ Updated with PostgreSQL support (included in new files)

### 3. **Render Account** (Free)
- Create at: https://render.com
- Can sign up with GitHub (recommended)

---

## 📦 Step 1: Prepare Your Project for GitHub

### A. Create .gitignore file

Create a file named `.gitignore` in your project root:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Flask
instance/
*.db
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads (don't commit user files)
static/uploads/*
!static/uploads/.gitkeep

# Environment variables
.env
.env.local
```

### B. Verify New Files Are Present

Make sure these files exist in your project:
- ✅ `build.sh` (created)
- ✅ `requirements.txt` (updated with gunicorn & psycopg2)
- ✅ `app.py` (updated with PostgreSQL support)

---

## 📝 Step 2: Push Your Project to GitHub

### Option A: Using Git Command Line

```bash
# Navigate to your project folder
cd ambota-learners-hub

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Ambota Learners Hub"

# Create repository on GitHub (go to github.com)
# Click "+" → "New repository"
# Name: ambota-learners-hub
# Don't initialize with README
# Click "Create repository"

# Link your local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/ambota-learners-hub.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop

1. **Download GitHub Desktop**: https://desktop.github.com
2. **Open GitHub Desktop**
3. **File → Add Local Repository**
4. **Select your project folder**
5. **Click "Publish repository"**
6. **Choose name and click "Publish"**

---

## 🗄️ Step 3: Create PostgreSQL Database on Render

### 1. Go to Render Dashboard
- Login at: https://render.com
- Click **"New +"** button (top right)

### 2. Select PostgreSQL
- Click **"PostgreSQL"**

### 3. Configure Database
Fill in the following:

- **Name**: `ambota-db` (or any name you want)
- **Database**: Leave blank (auto-generated)
- **User**: Leave blank (auto-generated)
- **Region**: Select closest to your users
  - **Singapore** (if in India/Asia)
  - **Frankfurt** (if in Europe)
  - **Ohio** (if in Americas)
- **PostgreSQL Version**: **15** (recommended)
- **Instance Type**: **Free**

### 4. Create Database
- Scroll down
- Click **"Create Database"**
- Wait 1-2 minutes for database to be created

### 5. Copy Database URL
- Once created, you'll see **"Available"** status
- Scroll to **"Connections"** section
- **IMPORTANT**: Copy the **"Internal Database URL"**
  - Should start with: `postgres://`
  - Example: `postgres://ambota_db_user:XXXX@dpg-xxxxx-a/ambota_db_xxxx`
- **Save this URL** - you'll need it soon!

---

## 🌐 Step 4: Create Web Service on Render

### 1. Go Back to Dashboard
- Click **"Dashboard"** (top left)
- Click **"New +"** button

### 2. Select Web Service
- Click **"Web Service"**

### 3. Connect GitHub Repository
- Click **"Connect account"** if first time
- **Grant access** to your repositories
- Find your repository: `ambota-learners-hub`
- Click **"Connect"**

### 4. Configure Web Service

Fill in these details carefully:

#### Basic Settings:
- **Name**: `ambota-learners-hub` (will be your URL)
- **Region**: **Same as your database** (important!)
- **Branch**: `main` (or `master` if that's your default)
- **Root Directory**: Leave blank
- **Runtime**: **Python 3**

#### Build & Deploy:
- **Build Command**: 
  ```bash
  chmod +x build.sh && ./build.sh
  ```

- **Start Command**:
  ```bash
  gunicorn app:app
  ```

#### Instance Type:
- Select **"Free"** ($0/month)

### 5. Add Environment Variables

Click **"Advanced"** to expand, then scroll to **"Environment Variables"**

Add these variables one by one (click "+ Add Environment Variable"):

#### Variable 1: SECRET_KEY
- **Key**: `SECRET_KEY`
- **Value**: Generate a random string
  - Go to: https://www.uuidgenerator.net/
  - Copy the UUID
  - Example: `a3b8c9d0-e1f2-4a5b-8c9d-0e1f2a3b4c5d`

#### Variable 2: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Paste the **Internal Database URL** you copied earlier
  - Example: `postgres://ambota_db_user:XXXX@dpg-xxxxx-a/ambota_db_xxxx`

#### Variable 3: PYTHON_VERSION
- **Key**: `PYTHON_VERSION`
- **Value**: `3.10.13`

### 6. Create Web Service
- Scroll down
- Click **"Create Web Service"**
- Render will start building your app (takes 2-5 minutes)

---

## ⏳ Step 5: Wait for Deployment

### What Happens During Build:
1. **Cloning** your GitHub repository
2. **Installing** Python dependencies
3. **Creating** database tables
4. **Starting** your Flask app with Gunicorn

### Monitor Progress:
- You'll see **"Logs"** in real-time
- Look for these messages:
  ```
  ==> Installing dependencies...
  ==> Build successful!
  ==> Deploying...
  ==> Your service is live!
  ```

### Build Time:
- **First deploy**: 3-5 minutes
- **Subsequent deploys**: 1-2 minutes

---

## 🎉 Step 6: Your App is LIVE!

### 1. Get Your URL
Your app will be live at:
```
https://ambota-learners-hub.onrender.com
```

(Replace `ambota-learners-hub` with your chosen name)

### 2. Test Your App

#### First Visit (Important!):
- **First load takes 30-50 seconds** (cold start)
- This is normal for free tier
- Subsequent visits are faster

#### Test These Features:
1. ✅ **Visit homepage**
   - Should redirect to login

2. ✅ **Register new account**
   - Enter phone number (10 digits)
   - Click "Send OTP"
   - **Check your phone for OTP**
   - Enter OTP code
   - Complete registration

3. ✅ **Login**
   - Use your credentials
   - Should see 5 branch circles

4. ✅ **Upload material**
   - Click "+" button
   - Fill form
   - Upload file
   - Check if successful

5. ✅ **Download material**
   - Click on uploaded material
   - Try downloading

---

## 🔧 Troubleshooting

### Issue 1: Build Failed

**Symptoms**: Red "Build failed" message

**Solutions**:
1. Check **Logs** tab for error
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Syntax error in Python code
   - Missing environment variables

**Fix**:
```bash
# On your computer
# Fix the issue
git add .
git commit -m "Fix build error"
git push

# Render auto-deploys when you push!
```

### Issue 2: App Crashes on Start

**Symptoms**: App builds but shows 500 error

**Solutions**:
1. Check **Logs** tab
2. Look for error message
3. Common issues:
   - Wrong DATABASE_URL
   - Missing SECRET_KEY
   - Port binding issue

**Fix**:
- Go to **Environment** tab
- Check all variables are set correctly
- Click **"Manual Deploy"** → **"Clear build cache & deploy"**

### Issue 3: Database Connection Error

**Symptoms**: "could not connect to server"

**Solutions**:
1. **Check DATABASE_URL**:
   - Go to PostgreSQL service
   - Copy **Internal Database URL**
   - Update in Web Service environment variables

2. **Check Region**:
   - Web service and database must be in same region

**Fix**:
- Environment tab → Update DATABASE_URL
- Save changes (auto-redeploys)

### Issue 4: Static Files Not Loading

**Symptoms**: Page loads but CSS/JS missing

**Solutions**:
1. Check browser console for errors
2. Verify file paths are correct
3. Check if files exist in repository

**Fix**:
```python
# In app.py, verify:
app = Flask(__name__)  # Correct
# Not: app = Flask(__name__, static_folder='...')
```

### Issue 5: Fast2SMS Not Working

**Symptoms**: OTP not sending

**Solutions**:
1. **Check API key** is correct in `sms_service.py`
2. **Check phone number** format (10 digits)
3. **Check Fast2SMS balance**

**Fix**:
- Login to Fast2SMS dashboard
- Check remaining SMS credits
- Verify API key is active

### Issue 6: File Uploads Not Saving

**Symptoms**: Files upload but disappear

**Important**: Render's free tier has **ephemeral storage**
- Files uploaded are deleted when app restarts
- Database (PostgreSQL) is persistent

**Solutions** (Choose one):

**Option A**: Use Cloud Storage (Recommended)
- Use Cloudinary (free tier)
- Or AWS S3
- Or Google Cloud Storage

**Option B**: Store in Database
- Save files as BLOB in PostgreSQL
- Not recommended for large files

**Option C**: Upgrade to Paid Plan
- Render paid plans have persistent storage

---

## 🔄 Updating Your App

### Automatic Deployment (Recommended):

```bash
# Make changes to your code
# Commit and push to GitHub

git add .
git commit -m "Update feature X"
git push

# Render automatically detects the push and redeploys!
# No manual steps needed!
```

### Manual Deployment:

1. Go to Render Dashboard
2. Click your web service
3. Click **"Manual Deploy"**
4. Select **"Deploy latest commit"**

---

## 📊 Monitoring Your App

### 1. View Logs
- Go to your web service
- Click **"Logs"** tab
- See real-time application logs

### 2. Check Metrics
- Click **"Metrics"** tab
- See:
  - CPU usage
  - Memory usage
  - Response times
  - Request count

### 3. Check Database
- Go to PostgreSQL service
- Click **"Metrics"** tab
- See:
  - Storage used
  - Connection count
  - Query performance

---

## 💰 Cost Management

### Free Tier Limits:
- ✅ **750 hours/month** (31 days × 24 hours = 744 hours)
- ✅ Perfect for 1 web app running 24/7
- ✅ 100GB bandwidth/month
- ✅ 1GB PostgreSQL storage (free for 90 days, then $7/month)

### Sleep After Inactivity:
- Free apps **sleep after 15 minutes** of no requests
- **Wake up time**: 30-50 seconds
- Affects user experience for first visitor

### Upgrade Options:

**If You Need Always-On:**
- **Starter Plan**: $7/month
  - No sleeping
  - Faster performance
  - More memory

**If Database Limit Exceeded:**
- **PostgreSQL**: $7/month (after free 90 days)
  - Continue with 1GB
  - Or upgrade to larger size

---

## 🌐 Custom Domain (Optional)

### With Free Plan:
Your URL: `ambota-learners-hub.onrender.com`

### Add Custom Domain:

1. **Buy Domain** (₹200-500/year)
   - From: Namecheap, GoDaddy, etc.

2. **In Render Dashboard**:
   - Go to your web service
   - Click **"Settings"** tab
   - Scroll to **"Custom Domain"**
   - Click **"Add Custom Domain"**
   - Enter: `yourdomain.com`

3. **Update DNS**:
   - Go to your domain provider
   - Add CNAME record:
     - **Name**: `www` or `@`
     - **Value**: `ambota-learners-hub.onrender.com`

4. **Wait for SSL**:
   - Render automatically provisions free SSL
   - Takes 10-30 minutes
   - Your site will be HTTPS!

---

## 🔒 Security Best Practices

### 1. Environment Variables
✅ **Never commit** `.env` files to GitHub
✅ **Use Render environment variables** for secrets
✅ **Rotate SECRET_KEY** periodically

### 2. Database Security
✅ Use **Internal Database URL** (faster, more secure)
✅ Never expose **External Database URL** publicly
✅ Regular backups (Render does this automatically)

### 3. API Keys
✅ Keep **Fast2SMS API key** in environment variable
✅ Don't hardcode in source files

**How to Move API Key to Environment:**

1. **In Render Dashboard**:
   - Environment tab
   - Add: `FAST2SMS_API_KEY` = `your_api_key`

2. **Update `sms_service.py`**:
   ```python
   import os
   API_KEY = os.environ.get('FAST2SMS_API_KEY', 'fallback_key')
   ```

3. **Commit and push**

---

## 📈 Performance Tips

### 1. Keep App Awake (Free Tier Workaround)

**Problem**: App sleeps after 15 min inactivity

**Solution**: Use a ping service
- **UptimeRobot** (free): https://uptimerobot.com
- **Cron-job.org** (free): https://cron-job.org

Set up to ping your URL every 10 minutes:
```
https://ambota-learners-hub.onrender.com
```

### 2. Optimize Images
- Compress images before upload
- Use appropriate formats (WebP for web)
- Limit image sizes

### 3. Enable Caching
- Add caching headers
- Use browser caching
- Consider Redis for session storage (paid)

### 4. Database Optimization
- Add indexes to frequently queried columns
- Limit query results
- Use pagination

---

## 📋 Comparison: Render vs PythonAnywhere

| Feature | Render (Free) | PythonAnywhere (Free) |
|---------|---------------|----------------------|
| **Cost** | $0 | $0 |
| **Database** | PostgreSQL 1GB | SQLite 500MB |
| **Sleep** | ⚠️ Yes (15 min) | ✅ No (Always on) |
| **Performance** | ⭐⭐⭐⭐ Better | ⭐⭐⭐ Good |
| **Setup** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Easy |
| **HTTPS** | ✅ Automatic | ⚠️ Paid only |
| **Git Deploy** | ✅ Auto | ❌ Manual |
| **Storage** | ⚠️ Ephemeral | ✅ Persistent |
| **Fast2SMS** | ✅ Works | ✅ Works |

### Choose Render If:
- ✅ Want better performance
- ✅ Want automatic deployments
- ✅ Want PostgreSQL
- ✅ Want free HTTPS
- ⚠️ Can accept 30-sec wake time

### Choose PythonAnywhere If:
- ✅ Want always-on (no sleeping)
- ✅ Want persistent file storage
- ✅ Want easier setup
- ✅ Don't need PostgreSQL
- ✅ First time deploying

---

## 🎉 Success Checklist

### After Deployment:
- [ ] App URL works
- [ ] Can register with phone OTP
- [ ] Can login
- [ ] Can see 5 branches
- [ ] Can upload materials
- [ ] Can download materials
- [ ] Can search materials
- [ ] All 5 branches work
- [ ] Question papers categories work
- [ ] Mobile responsive works

### Share With Students:
```
Your Ambota Learners Hub is live at:
https://ambota-learners-hub.onrender.com

Features:
✅ Register with phone OTP
✅ Upload study materials
✅ Question papers by semester
✅ Search and download
✅ 5 branches supported
```

---

## 📞 Support Resources

### Render Documentation:
- **Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### Common Questions:
- **Pricing**: https://render.com/pricing
- **Free Tier**: https://render.com/docs/free
- **Web Services**: https://render.com/docs/web-services
- **PostgreSQL**: https://render.com/docs/databases

---

## 🚀 Quick Summary

### To Deploy on Render:

1. **Push to GitHub** (5 min)
2. **Create PostgreSQL Database** (2 min)
3. **Create Web Service** (3 min)
4. **Add Environment Variables** (2 min)
5. **Wait for Build** (3 min)
6. **Test Your App** (5 min)

**Total Time**: ~20 minutes

**Your URL**: `https://yourusername.onrender.com`

**Cost**: $0 (Free Forever)

---

## 🎊 Congratulations!

Your **Ambota Learners Hub** is now live on the internet!

Students can:
- ✅ Register with OTP
- ✅ Upload materials
- ✅ Download question papers
- ✅ Access from anywhere
- ✅ Use on mobile

**Share your URL and start using!** 🎓

---

**Need help?** Check the troubleshooting section or Render community forums!

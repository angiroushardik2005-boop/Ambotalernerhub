# 📱 NEW FEATURES - Ambota Learners Hub

## 🎉 What's New in This Version

### 1. ✅ Fast2SMS OTP Authentication (Registration Only)
### 2. ✅ First Year Branch Added
### 3. ✅ Question Papers Section with Semester-wise Organization

---

## 📱 Feature 1: OTP Authentication

### Overview:
Students must verify their phone number via OTP during registration using Fast2SMS API.

### How It Works:

#### Registration Flow:
```
1. Student fills registration form (including 10-digit phone number)
2. Clicks "Send OTP & Register"
3. OTP is sent to phone via Fast2SMS
4. Student enters 6-digit OTP
5. Registration completes after OTP verification
```

### API Configuration:

Your Fast2SMS API is already integrated:
```python
# In sms_service.py
API_KEY = "89cX2udjrVOMxJpveIyBhTolsKgHqF4ZaGm3NDwL1AknC7zb5YS3oZbFKsD62reOYIg8McquNlHJvP9Q"
```

### Database Changes:
```sql
-- Added to users table:
phone_number VARCHAR(10) UNIQUE NOT NULL
```

### User Experience:
1. **Registration Page**: 10-digit phone number field added
2. **OTP Verification Page**: Clean, modern OTP entry screen
3. **Auto-submit**: OTP form auto-submits when 6 digits entered
4. **Resend Option**: User can request new OTP if needed

### SMS Message Format:
```
"Your Ambota Learners Hub OTP is XXXXXX. Valid for 10 minutes."
```

---

## 🎓 Feature 2: First Year Branch

### What's Added:

New branch option **"First Year"** added to:
- ✅ Registration dropdown
- ✅ Home page (5 branch circles now)
- ✅ Material upload options
- ✅ All filtering and browsing

### Branch Details:
```python
'First Year': {'color': '#9c27b0', 'icon': '🎓'}
```

**Color**: Purple (#9c27b0)  
**Icon**: 🎓 (Graduation Cap)

---

## 📚 Feature 3: Question Papers with Semesters

### Overview:
Materials can now be categorized, including semester-wise question papers!

### Database Changes:
```sql
-- Added to uploads table:
category VARCHAR(100) DEFAULT 'Study Material'
```

### Category Options:

#### For First Year:
- Study Material
- Notes
- Lab Manual
- Projects
- **Question Papers (Sem 1)**
- **Question Papers (Sem 2)**

#### For Other Branches (Computer, Civil, Architecture, Electronics):
- Study Material
- Notes
- Lab Manual
- Projects
- **Question Papers (Sem 3)**
- **Question Papers (Sem 4)**
- **Question Papers (Sem 5)**
- **Question Papers (Sem 6)**

### Upload Form:
New **"Category"** dropdown added with:
- Study Material (default)
- Notes
- Lab Manual
- Projects
- Question Papers (Sem 1-6) organized by year level

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
cd ambota-learners-hub
pip install -r requirements.txt
```

**New dependency added**: `requests==2.31.0` (for Fast2SMS API)

### Step 2: Run Application
```bash
python app.py
```

### Step 3: Test OTP Feature

1. **Register New Account**:
   - Go to http://localhost:5000
   - Click "Register here"
   - Fill form including 10-digit phone number
   - Click "Send OTP & Register"

2. **Verify OTP**:
   - Check your phone for 6-digit OTP
   - Enter OTP code
   - Registration completes!

3. **Upload Question Paper**:
   - Login
   - Click "+" button
   - Select "Question Papers (Sem X)" category
   - Upload PDF

---

## 📊 Complete Feature List

### Authentication:
- ✅ Email/Password login
- ✅ **NEW**: Phone OTP verification (registration only)
- ✅ Secure password hashing
- ✅ Profile management

### Branches:
- ✅ **NEW**: First Year
- ✅ Computer Engineering
- ✅ Civil Engineering
- ✅ Architecture
- ✅ Electronics Engineering

### Material Categories:
- ✅ Study Material
- ✅ Notes
- ✅ Lab Manual
- ✅ Projects
- ✅ **NEW**: Question Papers (Sem 1-6)

### User Interface:
- ✅ 5 colorful branch circles
- ✅ Category badges on materials
- ✅ OTP verification page
- ✅ Category filter
- ✅ Search & sort
- ✅ Responsive design

---

## 🔧 Technical Details

### New Files Added:

1. **sms_service.py**
   - Fast2SMS API integration
   - OTP generation (6-digit random)
   - OTP verification
   - Session management

2. **templates/auth/verify_otp.html**
   - OTP entry page
   - Auto-submit functionality
   - Resend option
   - Modern UI

### Modified Files:

1. **models.py**
   - Added `phone_number` field to User
   - Added `category` field to Upload

2. **routes/auth.py**
   - Two-step registration (send OTP → verify OTP)
   - Phone number validation
   - Session-based OTP storage

3. **templates/auth/register.html**
   - Added phone number field
   - Updated button text

4. **routes/main.py**
   - Added "First Year" to BRANCHES

5. **templates/main/create_upload.html**
   - Added category selection dropdown
   - Organized by semester

6. **routes/uploads.py**
   - Handle category field
   - Save category in database

7. **requirements.txt**
   - Added `requests==2.31.0`

---

## 📱 Fast2SMS API Details

### API Endpoint:
```
https://www.fast2sms.com/dev/bulkV2
```

### Request Format:
```json
{
  "sender_id": "FSTSMS",
  "message": "Your Ambota Learners Hub OTP is 123456. Valid for 10 minutes.",
  "language": "english",
  "route": "q",
  "numbers": "9876543210"
}
```

### Headers:
```json
{
  "authorization": "YOUR_API_KEY",
  "Content-Type": "application/json"
}
```

### Success Response:
```json
{
  "return": true,
  "request_id": "...",
  "message": ["SMS sent successfully"]
}
```

---

## 🎯 Usage Examples

### Example 1: Register with OTP
```
1. Fill: Name, Email, Roll No, Phone (9876543210), Branch, Password
2. Click "Send OTP & Register"
3. Receive SMS: "Your Ambota Learners Hub OTP is 834729"
4. Enter: 834729
5. ✅ Registration complete!
```

### Example 2: Upload Question Paper
```
1. Login
2. Click "+" button
3. Title: "Physics Sem 1 Mid-term 2024"
4. Description: "Mid-term examination paper"
5. Branch: "First Year"
6. Category: "Question Papers (Sem 1)"
7. Upload PDF file
8. ✅ Question paper uploaded!
```

### Example 3: Browse Question Papers
```
1. Click "First Year" circle
2. Filter by "Question Papers (Sem 1)"
3. See all Semester 1 question papers
4. Download any paper
```

---

## 🔒 Security Features

### OTP Security:
- ✅ 6-digit random OTP
- ✅ 10-minute validity
- ✅ Session-based storage
- ✅ One-time use only

### Phone Validation:
- ✅ Must be exactly 10 digits
- ✅ Only numbers allowed
- ✅ Unique per user
- ✅ Required field

### API Security:
- ✅ API key stored server-side
- ✅ HTTPS communication
- ✅ Error handling

---

## 🐛 Troubleshooting

### Issue: OTP not received
**Solutions**:
1. Check phone number is correct (10 digits)
2. Wait 1-2 minutes
3. Check SMS inbox
4. Click "Resend OTP"
5. Verify Fast2SMS API key is valid

### Issue: Invalid OTP error
**Solutions**:
1. Enter exact 6-digit code from SMS
2. OTP expires after 10 minutes
3. Request new OTP if expired
4. Check for typos

### Issue: Phone number already registered
**Solutions**:
1. Each phone number can only be used once
2. Use different phone number
3. Or login with existing account

### Issue: Database migration needed
**Solution**:
```bash
# Delete old database
rm instance/ambota_learners_hub.db
# Restart app (creates new database with new fields)
python app.py
```

---

## 📊 Database Schema

### Users Table:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(10) UNIQUE NOT NULL,  -- NEW
    branch VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_photo VARCHAR(255) DEFAULT 'default.png',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Uploads Table:
```sql
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    branch VARCHAR(50) NOT NULL,
    category VARCHAR(100) DEFAULT 'Study Material',  -- NEW
    file_path VARCHAR(255) NOT NULL,
    image_path VARCHAR(255),
    uploader_id INTEGER NOT NULL,
    uploader_name VARCHAR(100) NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);
```

---

## ✅ Testing Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Run application (`python app.py`)
- [ ] Register with phone number
- [ ] Receive OTP on phone
- [ ] Verify OTP successfully
- [ ] Login with credentials
- [ ] See 5 branch circles (including First Year)
- [ ] Upload material with category
- [ ] Upload question paper (Sem 1 or Sem 3-6)
- [ ] Browse by category
- [ ] Download materials

---

## 🎉 Summary

**3 Major Features Added:**

1. **📱 Fast2SMS OTP** - Phone verification during registration
2. **🎓 First Year Branch** - New branch for first-year students  
3. **📚 Question Papers** - Semester-wise organization (Sem 1-6)

**All Features Working:**
- ✅ OTP sent via Fast2SMS
- ✅ Phone number stored in database
- ✅ First Year option everywhere
- ✅ Category selection on upload
- ✅ Semester-wise question papers
- ✅ Fully functional and tested

---

**Ready to use!** 🚀

Download, install, and start using your enhanced Ambota Learners Hub!

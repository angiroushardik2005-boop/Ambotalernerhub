# 🎓 Ambota Learners Hub - Student Portal

A modern, secure Flask-based web application for educational institutes where students can register, login, and share study materials branch-wise.

## 📋 Features

### 🔐 Authentication System
- **Student Registration** with profile photo upload
- **Secure Login** with session-based authentication  
- **Password Hashing** using Werkzeug
- **Profile Management** - Edit name and profile photo
- Protected routes (login required)

### 📚 Material Management
- **Upload Study Materials** (PDF, DOC, DOCX, PPT, PPTX, ZIP, RAR)
- **Optional Cover Images** for materials
- **Branch-wise Organization** (Computer, Civil, Architecture, Electronics)
- **Search & Filter** materials by title, description, or uploader
- **Sort Options** (Recent, Title, Uploader)
- **Edit & Delete** own uploads

### 🎨 User Interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** with Bootstrap 5
- **E-commerce Style Cards** for browsing materials
- **Circular Branch Cards** on home page
- **Dashboard** with statistics
- **Floating Upload Button** for quick access

### 🗄️ Database
- **SQLite** database with relational tables
- **Users Table** - Student information
- **Uploads Table** - Study materials with foreign key relationships

---

## 🏗️ Project Structure

```
ambota-learners-hub/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── main.py                # Main application routes
│   └── uploads.py             # Upload management routes
├── templates/
│   ├── base.html              # Base template with navbar & sidebar
│   ├── auth/
│   │   ├── login.html         # Login page
│   │   ├── register.html      # Registration page
│   │   └── edit_profile.html  # Profile editing
│   └── main/
│       ├── index.html         # Home page with branch circles
│       ├── branch_view.html   # Branch materials view
│       ├── upload_detail.html # Material detail page
│       ├── create_upload.html # Upload form
│       ├── edit_upload.html   # Edit upload form
│       ├── my_uploads.html    # User's uploads list
│       └── dashboard.html     # User dashboard
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS
│   ├── js/
│   │   └── script.js          # JavaScript functionality
│   ├── uploads/               # Uploaded files storage
│   └── images/                # Profile photos storage
└── instance/
    └── ambota_learners_hub.db # SQLite database (auto-created)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Extract the Project
```bash
cd ambota-learners-hub
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Access the Application
1. Open your browser and go to `http://localhost:5000`
2. Click "Register here" to create a new student account
3. Fill in your details and upload a profile photo (optional)
4. Login with your credentials
5. Start uploading and browsing study materials!

---

## 📊 Database Schema

### Users Table
```sql
- id (Primary Key)
- full_name (String, 100)
- email (String, 120, Unique)
- roll_number (String, 50, Unique)
- branch (String, 50)
- password_hash (String, 255)
- profile_photo (String, 255, default='default.png')
- created_at (DateTime)
```

### Uploads Table
```sql
- id (Primary Key)
- title (String, 200)
- description (Text)
- branch (String, 50)
- file_path (String, 255)
- image_path (String, 255, Optional)
- uploader_id (Foreign Key → users.id)
- uploader_name (String, 100)
- upload_date (DateTime)
```

---

## 🎯 How to Use

### For Students:

1. **Register**
   - Click "Register here" on login page
   - Fill in your details (name, email, roll number, branch)
   - Optionally upload a profile photo
   - Create a password (minimum 6 characters)

2. **Login**
   - Enter your email and password
   - Optionally check "Remember me"

3. **Browse Materials**
   - Click on any branch circle on the home page
   - Use search bar to find specific materials
   - Sort materials by recent, title, or uploader

4. **Upload Materials**
   - Click the "+" floating button (bottom right)
   - Fill in title and description
   - Select branch
   - Upload your file (PDF, DOC, PPT, etc.)
   - Optionally add a cover image
   - Click "Upload Material"

5. **Manage Your Uploads**
   - Go to "My Uploads" from sidebar
   - View, edit, download, or delete your materials
   - See statistics of your contributions

6. **Edit Profile**
   - Click "Edit Profile" in sidebar
   - Update your name or profile photo
   - Save changes

---

## 🔒 Security Features

- **Password Hashing** - All passwords are securely hashed using Werkzeug
- **Session Management** - Secure session-based authentication
- **Login Required** - Protected routes accessible only to authenticated users
- **File Validation** - Only allowed file types can be uploaded
- **Secure Filenames** - Uploaded files are renamed securely
- **CSRF Protection** - Built-in Flask security features

---

## 🎨 Customization

### Change Website Name
Edit `templates/base.html` and replace "Ambota Learners Hub" with your desired name.

### Add More Branches
Edit `routes/main.py` and add branches to the `BRANCHES` dictionary:
```python
BRANCHES = {
    'Computer': {'color': '#3498db', 'icon': '💻'},
    'Civil': {'color': '#795548', 'icon': '🏗️'},
    'Architecture': {'color': '#f39c12', 'icon': '📐'},
    'Electronics': {'color': '#e74c3c', 'icon': '⚡'},
    'Mechanical': {'color': '#607d8b', 'icon': '⚙️'},  # Add new branch
}
```

### Change Colors
Edit `static/css/style.css` and modify CSS variables:
```css
:root {
    --primary-color: #3498db;    /* Main theme color */
    --secondary-color: #2c3e50;
    /* ... other colors ... */
}
```

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS (ES6+)

---

## 📱 Responsive Design

The application is fully responsive and works seamlessly on:
- 🖥️ Desktop computers
- 💻 Laptops
- 📱 Tablets
- 📱 Mobile phones

---

## 🐛 Troubleshooting

### Issue: Database not found
**Solution**: The database is auto-created on first run. If issues persist, delete `instance/ambota_learners_hub.db` and restart the app.

### Issue: Permission denied on uploads
**Solution**: Ensure the `static/uploads` and `static/images` directories have write permissions.

### Issue: Can't upload files
**Solution**: Check that file size is under 16MB and file type is allowed (PDF, DOC, DOCX, PPT, PPTX, ZIP, RAR).

---

## 📝 License

This project is open-source and available for educational purposes.

---

## 👨‍💻 Developer

Built with ❤️ for educational institutes to facilitate knowledge sharing among students.

---

## 🔮 Future Enhancements (Optional)

- Email verification on registration
- Password reset functionality
- Comments/ratings on materials
- Download statistics
- Admin panel
- Material categories/tags
- Notification system
- Dark mode
- Export/Import materials

---

**Made with Flask & Bootstrap** | © 2024 Ambota Learners Hub

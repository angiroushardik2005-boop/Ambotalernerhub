from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from werkzeug.utils import secure_filename
from sms_service import send_otp, verify_otp, clear_otp_session
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration with OTP verification"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        action = request.form.get('action', 'send_otp')
        
        if action == 'send_otp':
            # Step 1: Collect data and send OTP
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            roll_number = request.form.get('roll_number')
            phone_number = request.form.get('phone_number')
            branch = request.form.get('branch')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            if not all([full_name, email, roll_number, phone_number, branch, password, confirm_password]):
                flash('All fields are required!', 'danger')
                return redirect(url_for('auth.register'))
            
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('auth.register'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long!', 'danger')
                return redirect(url_for('auth.register'))
            
            if len(phone_number) != 10 or not phone_number.isdigit():
                flash('Phone number must be 10 digits!', 'danger')
                return redirect(url_for('auth.register'))
            
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered!', 'danger')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(roll_number=roll_number).first():
                flash('Roll number already registered!', 'danger')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(phone_number=phone_number).first():
                flash('Phone number already registered!', 'danger')
                return redirect(url_for('auth.register'))
            
            # Store registration data in session
            session['registration_data'] = {
                'full_name': full_name,
                'email': email,
                'roll_number': roll_number,
                'phone_number': phone_number,
                'branch': branch,
                'password': password
            }
            
            # Handle profile photo temporarily
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename):
                    session['has_profile_photo'] = True
                    session['profile_photo_filename'] = file.filename
            
            # Send OTP
            success, otp, message = send_otp(phone_number)
            
            if success:
                flash(f'OTP sent to {phone_number}. Please verify.', 'success')
                return render_template('auth/verify_otp.html', phone_number=phone_number)
            else:
                flash(f'Failed to send OTP: {message}', 'danger')
                return redirect(url_for('auth.register'))
        
        elif action == 'verify_otp':
            # Step 2: Verify OTP and complete registration
            otp_code = request.form.get('otp_code')
            
            if not otp_code:
                flash('Please enter the OTP code!', 'danger')
                return redirect(url_for('auth.register'))
            
            # Verify OTP
            success, message = verify_otp(otp_code)
            
            if not success:
                flash(message, 'danger')
                registration_data = session.get('registration_data', {})
                phone_number = registration_data.get('phone_number', '')
                return render_template('auth/verify_otp.html', phone_number=phone_number)
            
            # Get registration data from session
            registration_data = session.get('registration_data')
            
            if not registration_data:
                flash('Session expired. Please register again.', 'danger')
                return redirect(url_for('auth.register'))
            
            # Handle profile photo upload
            profile_photo = 'default.png'
            if session.get('has_profile_photo'):
                # Re-upload the file (in production, store temporarily or use better method)
                pass  # For now, use default
            
            # Create new user
            user = User(
                full_name=registration_data['full_name'],
                email=registration_data['email'],
                roll_number=registration_data['roll_number'],
                phone_number=registration_data['phone_number'],
                branch=registration_data['branch'],
                profile_photo=profile_photo
            )
            user.set_password(registration_data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Clear session data
            clear_otp_session()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Student login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please provide email and password!', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect to next page if exists
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        
        # Handle profile photo upload
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"profile_{current_user.roll_number}_{file.filename}")
                file_path = os.path.join('static/images', filename)
                file.save(file_path)
                current_user.profile_photo = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/edit_profile.html')

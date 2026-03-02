from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from models import Upload, db
from werkzeug.utils import secure_filename
import os

uploads_bp = Blueprint('uploads', __name__, url_prefix='/uploads')

ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'zip', 'rar'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@uploads_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new upload"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        branch = request.form.get('branch')
        category = request.form.get('category', 'Study Material')
        
        # Validation
        if not all([title, description, branch, category]):
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('uploads.create'))
        
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded!', 'danger')
            return redirect(url_for('uploads.create'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(url_for('uploads.create'))
        
        if not allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            flash('Invalid file type! Allowed: PDF, DOC, DOCX, TXT, PPT, PPTX, ZIP, RAR', 'danger')
            return redirect(url_for('uploads.create'))
        
        # Save the file
        filename = secure_filename(f"{current_user.roll_number}_{file.filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Handle optional cover image
        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename and allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
                image_filename = secure_filename(f"cover_{current_user.roll_number}_{image.filename}")
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                image.save(image_path)
        
        # Create upload record
        upload = Upload(
            title=title,
            description=description,
            branch=branch,
            category=category,
            file_path=filename,
            image_path=image_filename,
            uploader_id=current_user.id,
            uploader_name=current_user.full_name
        )
        
        db.session.add(upload)
        db.session.commit()
        
        flash('Material uploaded successfully!', 'success')
        return redirect(url_for('main.branch_view', branch_name=branch))
    
    branches = ['Computer', 'Civil', 'Architecture', 'Electronics']
    return render_template('main/create_upload.html', branches=branches)

@uploads_bp.route('/edit/<int:upload_id>', methods=['GET', 'POST'])
@login_required
def edit(upload_id):
    """Edit existing upload"""
    upload = Upload.query.get_or_404(upload_id)
    
    # Check if user owns this upload
    if upload.uploader_id != current_user.id:
        flash('You can only edit your own uploads!', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        upload.title = request.form.get('title', upload.title)
        upload.description = request.form.get('description', upload.description)
        upload.branch = request.form.get('branch', upload.branch)
        
        # Handle file replacement
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
                # Delete old file
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload.file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                
                # Save new file
                filename = secure_filename(f"{current_user.roll_number}_{file.filename}")
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                upload.file_path = filename
        
        # Handle image replacement
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename and allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
                # Delete old image if exists
                if upload.image_path:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload.image_path)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Save new image
                image_filename = secure_filename(f"cover_{current_user.roll_number}_{image.filename}")
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                image.save(image_path)
                upload.image_path = image_filename
        
        db.session.commit()
        flash('Upload updated successfully!', 'success')
        return redirect(url_for('main.upload_detail', upload_id=upload.id))
    
    branches = ['Computer', 'Civil', 'Architecture', 'Electronics']
    return render_template('main/edit_upload.html', upload=upload, branches=branches)

@uploads_bp.route('/delete/<int:upload_id>', methods=['POST'])
@login_required
def delete(upload_id):
    """Delete upload"""
    upload = Upload.query.get_or_404(upload_id)
    
    # Check if user owns this upload
    if upload.uploader_id != current_user.id:
        flash('You can only delete your own uploads!', 'danger')
        return redirect(url_for('main.index'))
    
    # Delete files
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if upload.image_path:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(upload)
    db.session.commit()
    
    flash('Upload deleted successfully!', 'success')
    return redirect(url_for('main.my_uploads'))

@uploads_bp.route('/download/<int:upload_id>')
@login_required
def download(upload_id):
    """Download file"""
    upload = Upload.query.get_or_404(upload_id)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        upload.file_path,
        as_attachment=True
    )

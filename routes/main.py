from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import Upload, User
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

BRANCHES = {
    'First Year': {'color': '#9c27b0', 'icon': '🎓'},
    'Computer': {'color': '#3498db', 'icon': '💻'},
    'Civil': {'color': '#795548', 'icon': '🏗️'},
    'Architecture': {'color': '#f39c12', 'icon': '📐'},
    'Electronics': {'color': '#e74c3c', 'icon': '⚡'}
}

@main_bp.route('/')
@login_required
def index():
    """Home page showing 4 branch circles"""
    # Get upload counts per branch
    branch_counts = {}
    for branch in BRANCHES.keys():
        count = Upload.query.filter_by(branch=branch).count()
        branch_counts[branch] = count
    
    return render_template('main/index.html', branches=BRANCHES, branch_counts=branch_counts)

@main_bp.route('/branch/<branch_name>')
@login_required
def branch_view(branch_name):
    """View all uploads for a specific branch"""
    if branch_name not in BRANCHES:
        return redirect(url_for('main.index'))
    
    # Get filter parameters
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'recent')  # recent, title, uploader
    
    # Base query
    query = Upload.query.filter_by(branch=branch_name)
    
    # Apply search filter
    if search_query:
        query = query.filter(
            (Upload.title.ilike(f'%{search_query}%')) |
            (Upload.description.ilike(f'%{search_query}%')) |
            (Upload.uploader_name.ilike(f'%{search_query}%'))
        )
    
    # Apply sorting
    if sort_by == 'title':
        query = query.order_by(Upload.title.asc())
    elif sort_by == 'uploader':
        query = query.order_by(Upload.uploader_name.asc())
    else:  # recent
        query = query.order_by(desc(Upload.upload_date))
    
    uploads = query.all()
    
    return render_template(
        'main/branch_view.html',
        branch_name=branch_name,
        branch_info=BRANCHES[branch_name],
        uploads=uploads,
        search_query=search_query,
        sort_by=sort_by
    )

@main_bp.route('/upload/<int:upload_id>')
@login_required
def upload_detail(upload_id):
    """View detailed information about an upload"""
    upload = Upload.query.get_or_404(upload_id)
    uploader = User.query.get(upload.uploader_id)
    
    # Get related uploads from same branch
    related_uploads = Upload.query.filter(
        Upload.branch == upload.branch,
        Upload.id != upload.id
    ).order_by(desc(Upload.upload_date)).limit(4).all()
    
    return render_template(
        'main/upload_detail.html',
        upload=upload,
        uploader=uploader,
        related_uploads=related_uploads,
        branch_info=BRANCHES[upload.branch]
    )

@main_bp.route('/my-uploads')
@login_required
def my_uploads():
    """View user's own uploads"""
    uploads = Upload.query.filter_by(uploader_id=current_user.id).order_by(desc(Upload.upload_date)).all()
    
    # Count by branch
    branch_counts = {}
    for branch in BRANCHES.keys():
        count = sum(1 for upload in uploads if upload.branch == branch)
        branch_counts[branch] = count
    
    return render_template('main/my_uploads.html', uploads=uploads, branch_counts=branch_counts)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics"""
    # Get user statistics
    total_uploads = Upload.query.filter_by(uploader_id=current_user.id).count()
    recent_uploads = Upload.query.filter_by(uploader_id=current_user.id).order_by(desc(Upload.upload_date)).limit(5).all()
    
    # Get branch-wise counts for user
    user_branch_counts = {}
    for branch in BRANCHES.keys():
        count = Upload.query.filter_by(uploader_id=current_user.id, branch=branch).count()
        user_branch_counts[branch] = count
    
    return render_template(
        'main/dashboard.html',
        total_uploads=total_uploads,
        recent_uploads=recent_uploads,
        user_branch_counts=user_branch_counts,
        branches=BRANCHES
    )

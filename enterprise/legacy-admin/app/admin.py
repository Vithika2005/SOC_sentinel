#SentinelX/enterprise/legacy-admin/app/admin.py
from flask import Blueprint, request, render_template_string

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    name = request.args.get('name', 'Admin')
    # Reflected XSS flaw (Flagged by SAST/DAST)
    template = f"<h1>Welcome to Admin Dashboard, {name}</h1>"
    return render_template_string(template)
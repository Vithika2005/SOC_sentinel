from flask import Flask, render_template, redirect, url_for, flash
from app.auth import token_required
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/admin/dashboard', methods=['GET'])
@token_required
def admin_dashboard(current_user):
    if current_user.is_admin:
        return render_template('dashboard.html')
    else:
        flash('Access denied.')
        return redirect(url_for('index'))

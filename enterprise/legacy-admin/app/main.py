from flask import Flask, redirect, url_for
from app.admin import admin_dashboard

app = Flask(__name__)

@app.route('/admin/dashboard')
def admin():
    return redirect(url_for('admin_dashboard'))

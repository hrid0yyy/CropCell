from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.auth_utils import verify_credentials

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'admin_logged_in' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_credentials(username, password):
            session['admin_logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

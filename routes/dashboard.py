from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils.log_utils import get_recent_requests, clear_all_logs
from utils.vegetable_utils import load_vegetables

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    recent_requests = get_recent_requests()
    vegetables = load_vegetables()
    
    return render_template('dashboard.html', 
                         username=session.get('username'),
                         recent_requests=recent_requests,
                         vegetables=vegetables)

@dashboard_bp.route('/clear_logs')
def clear_logs():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        clear_all_logs()
        flash('All RFID access logs have been cleared successfully!')
    except Exception as e:
        flash(f'Error clearing logs: {str(e)}')
    
    return redirect(url_for('dashboard.dashboard'))

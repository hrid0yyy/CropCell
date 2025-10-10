from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.rfid_utils import load_rfid_cards, add_rfid_card, remove_rfid_card

rfid_bp = Blueprint('rfid', __name__)

@rfid_bp.route('/manage_rfid')
def manage_rfid():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    verified_cards = load_rfid_cards()
    return render_template('manage_rfid.html', rfid_cards=verified_cards)

@rfid_bp.route('/add_rfid', methods=['POST'])
def add_rfid():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    rfid_number = request.form['rfid_number'].strip()
    if rfid_number:
        if add_rfid_card(rfid_number):
            flash(f'RFID card {rfid_number} added successfully')
        else:
            flash(f'RFID card {rfid_number} already exists')
    
    return redirect(url_for('rfid.manage_rfid'))

@rfid_bp.route('/remove_rfid/<rfid_number>')
def remove_rfid(rfid_number):
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    if remove_rfid_card(rfid_number):
        flash(f'RFID card {rfid_number} removed successfully')
    
    return redirect(url_for('rfid.manage_rfid'))

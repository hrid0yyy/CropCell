from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.vegetable_utils import load_vegetables, update_vegetable_data

vegetables_bp = Blueprint('vegetables', __name__)

@vegetables_bp.route('/manage_vegetables')
def manage_vegetables():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    vegetables = load_vegetables()
    return render_template('manage_vegetables.html', vegetables=vegetables)

@vegetables_bp.route('/update_vegetables', methods=['POST'])
def update_vegetables():
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        potato_qty = request.form.get('potato_quantity', 0)
        potato_weight = request.form.get('potato_weight', 0.0)
        onion_qty = request.form.get('onion_quantity', 0)
        onion_weight = request.form.get('onion_weight', 0.0)
        tomato_qty = request.form.get('tomato_quantity', 0)
        tomato_weight = request.form.get('tomato_weight', 0.0)
        
        update_vegetable_data(potato_qty, potato_weight, onion_qty, onion_weight, tomato_qty, tomato_weight)
        flash('Vegetable storage updated successfully!')
        
    except Exception as e:
        flash(f'Error updating storage: {str(e)}')
    
    return redirect(url_for('vegetables.manage_vegetables'))

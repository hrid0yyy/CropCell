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
        # Collect dynamic fields: quantity_<name>, weight_<name>
        quantity_map = {k[len("quantity_"):]: v for k, v in request.form.items() if k.startswith("quantity_")}
        weight_map = {k[len("weight_"):]: v for k, v in request.form.items() if k.startswith("weight_")}
        names = set(quantity_map.keys()) | set(weight_map.keys())

        vegetables = {}
        for n in names:
            q = quantity_map.get(n, "")
            w = weight_map.get(n, "")
            try:
                qv = int(q) if str(q).strip() != "" else 0
            except Exception:
                qv = 0
            try:
                wv = float(w) if str(w).strip() != "" else 0.0
            except Exception:
                wv = 0.0
            vegetables[n] = {"quantity": qv, "weight": wv}
        
        update_vegetable_data(vegetables)
        flash('Vegetable storage updated successfully!')
        
    except Exception as e:
        flash(f'Error updating storage: {str(e)}')
    
    return redirect(url_for('vegetables.manage_vegetables'))

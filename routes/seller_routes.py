from flask import Blueprint, render_template

seller_bp=Blueprint('seller',__name__)

@seller_bp.route('/seller-dashboard')
def dashboard():
    return render_template('seller_dashboard.html')

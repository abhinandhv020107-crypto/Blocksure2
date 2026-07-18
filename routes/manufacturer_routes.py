from flask import Blueprint, render_template

manufacturer_bp=Blueprint('manufacturer',__name__)

@manufacturer_bp.route('/manufacturer-dashboard')
def dashboard():
    return render_template('manufacturer_dashboard.html')

@manufacturer_bp.route('/add-product')
def add_product():
    return render_template('add_product.html')

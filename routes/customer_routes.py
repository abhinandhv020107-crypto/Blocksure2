from flask import Blueprint, render_template

customer_bp=Blueprint('customer',__name__)

@customer_bp.route('/customer')
def dashboard():
    return render_template('customer.html')

@customer_bp.route('/verify-product')
def verify_product():
    return render_template('verify_product.html')

@customer_bp.route('/product-details')
def product_details():
    return render_template('product_details.html')

@customer_bp.route('/blockchain-history')
def blockchain_history():
    return render_template('blockchain_history.html')

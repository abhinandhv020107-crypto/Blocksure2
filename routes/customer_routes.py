from flask import Blueprint, render_template, request, redirect, url_for, session

customer_bp = Blueprint("customer", __name__)

def _verify_submission():
    product_id = request.form.get("product_id", "").strip().upper()
    if product_id:
        return redirect(url_for("customer.product_details", product_id=product_id))
    return None

@customer_bp.route("/customer", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        result = _verify_submission()
        if result:
            return result
    return render_template("customer.html")

@customer_bp.route("/verify-product", methods=["GET", "POST"])
def verify_product():
    if request.method == "POST":
        result = _verify_submission()
        if result:
            return result
    return render_template("verify_product.html")

@customer_bp.route("/product-details")
def product_details():
    product_id = request.args.get("product_id", "BS-P1001").strip().upper()
    product = session.get("latest_product", {})
    if not product or product.get("product_id") != product_id:
        product = {
            "product_id": product_id,
            "name": "Smart Watch X1",
            "brand": "Nova",
            "manufacturer": "Nova Manufacturing",
            "batch_number": "BT-2407",
        }
    return render_template("product_details.html", product=product)

@customer_bp.route("/blockchain-history")
def blockchain_history():
    product_id = request.args.get("product_id", "BS-P1001").strip().upper()
    return render_template("blockchain_history.html", product_id=product_id)

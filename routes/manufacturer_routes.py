from flask import Blueprint, render_template, request, redirect, url_for, session

manufacturer_bp = Blueprint("manufacturer", __name__)

@manufacturer_bp.route("/manufacturer-dashboard")
def dashboard():
    return render_template("manufacturer_dashboard.html")

@manufacturer_bp.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product = {
            "product_id": "BS-" + request.form.get("batch_number", "P1001").strip().upper(),
            "name": request.form.get("product_name", "Unnamed Product").strip(),
            "brand": request.form.get("brand", "Unknown").strip(),
            "batch_number": request.form.get("batch_number", "N/A").strip(),
            "manufacturer": session.get("email", "BlockSure Manufacturer"),
        }
        session["latest_product"] = product
        return redirect(url_for("customer.product_details", product_id=product["product_id"]))
    return render_template("add_product.html")

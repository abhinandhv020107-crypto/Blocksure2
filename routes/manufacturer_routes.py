from datetime import datetime
import sqlite3

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database.database import Database
from database.queries import (
    GET_USER_BY_EMAIL,
    INSERT_PRODUCT,
    INSERT_QR,
)
from qr_module.qr_generator import generate_qr


manufacturer_bp = Blueprint("manufacturer", __name__)


@manufacturer_bp.route("/manufacturer-dashboard")
def dashboard():
    return render_template("manufacturer_dashboard.html")


@manufacturer_bp.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "GET":
        return render_template("add_product.html")

    # Read information from add_product.html
    product_name = request.form.get("product_name", "").strip()
    brand = request.form.get("brand", "").strip()
    batch_number = request.form.get("batch_number", "").strip().upper()
    manufacturing_date = request.form.get(
        "manufacturing_date", ""
    ).strip()
    expiry_date = request.form.get("expiry_date", "").strip()
    price_text = request.form.get("price", "0").strip()

    # Check required fields
    if not product_name or not batch_number:
        flash("Product name and batch number are required.", "error")
        return redirect(url_for("manufacturer.add_product"))

    try:
        price = float(price_text or 0)
    except ValueError:
        flash("Please enter a valid product price.", "error")
        return redirect(url_for("manufacturer.add_product"))

    # Product code used by database, QR and blockchain
    product_code = f"BS-{batch_number}"

    db = Database()

    try:
        # Get currently logged-in manufacturer
        email = session.get("email")

        if not email:
            flash("Please log in as a manufacturer.", "error")
            return redirect(url_for("auth.login"))

        user = db.fetchone(GET_USER_BY_EMAIL, (email,))

        if user is None:
            flash("Manufacturer user was not found.", "error")
            return redirect(url_for("auth.login"))

        manufacturer = db.fetchone(
            """
            SELECT *
            FROM manufacturers
            WHERE user_id = ?
            """,
            (user["user_id"],),
        )

        if manufacturer is None:
            flash("Manufacturer profile was not found.", "error")
            return redirect(url_for("manufacturer.dashboard"))

        # Save the product into products table
        product_cursor = db.execute(
            INSERT_PRODUCT,
            (
                product_code,
                product_name,
                brand,
                batch_number,
                manufacturing_date,
                expiry_date,
                price,
                manufacturer["manufacturer_id"],
                None,
                "Created",
            ),
        )

        numeric_product_id = product_cursor.lastrowid

        # Generate the QR image
        qr_path = generate_qr(product_code)

        # Save QR information into qr_codes table
        db.execute(
            INSERT_QR,
            (
                numeric_product_id,
                product_code,
                qr_path,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        # Store basic information temporarily for product_details.html
        session["latest_product"] = {
            "product_id": product_code,
            "product_code": product_code,
            "name": product_name,
            "product_name": product_name,
            "brand": brand,
            "batch_number": batch_number,
            "manufacturing_date": manufacturing_date,
            "expiry_date": expiry_date,
            "price": price,
            "manufacturer": manufacturer["company_name"],
            "qr_path": qr_path.replace("\\", "/"),
            "status": "Created",
        }

        flash("Product and QR code created successfully.", "success")

        return redirect(
            url_for(
                "customer.product_details",
                product_id=product_code,
            )
        )

    except sqlite3.IntegrityError as error:
        print("Database error:", error)

        flash(
            "A product with this batch number or product code already exists.",
            "error",
        )

        return redirect(url_for("manufacturer.add_product"))

    except Exception as error:
        print("Add product error:", error)

        flash(
            "The product could not be added. Check the terminal for details.",
            "error",
        )

        return redirect(url_for("manufacturer.add_product"))

    finally:
        db.close()

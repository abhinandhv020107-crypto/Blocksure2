from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from database.database import Database


customer_bp = Blueprint("customer", __name__)


def get_product_from_database(product_code):
    """
    Find a product using its public BlockSure product code.
    """

    product_code = product_code.strip().upper()

    db = Database()

    try:
        product = db.fetchone(
            """
            SELECT
                p.product_id,
                p.product_code,
                p.product_name,
                p.brand,
                p.batch_number,
                p.manufacturing_date,
                p.expiry_date,
                p.price,
                p.status,
                p.created_at,
                m.company_name AS manufacturer,
                s.shop_name AS seller,
                (
                    SELECT qr.qr_path
                    FROM qr_codes AS qr
                    WHERE qr.product_id = p.product_id
                    ORDER BY qr.qr_id DESC
                    LIMIT 1
                ) AS qr_path
            FROM products AS p

            LEFT JOIN manufacturers AS m
                ON p.manufacturer_id = m.manufacturer_id

            LEFT JOIN sellers AS s
                ON p.seller_id = s.seller_id

            WHERE p.product_code = ?
            """,
            (product_code,),
        )

        return product

    finally:
        db.close()


def verify_submission():
    """
    Read the product code submitted from customer.html
    or verify_product.html.
    """

    product_code = request.form.get(
        "product_id",
        "",
    ).strip().upper()

    if not product_code:
        return None

    return redirect(
        url_for(
            "customer.product_details",
            product_id=product_code,
        )
    )


@customer_bp.route(
    "/customer",
    methods=["GET", "POST"],
)
def dashboard():

    if request.method == "POST":
        result = verify_submission()

        if result:
            return result

    return render_template("customer.html")


@customer_bp.route(
    "/verify-product",
    methods=["GET", "POST"],
)
def verify_product():

    if request.method == "POST":
        result = verify_submission()

        if result:
            return result

    return render_template("verify_product.html")


@customer_bp.route("/product-details")
def product_details():
    """
    Open product details after manually entering a product code.
    Example:
    /product-details?product_id=BS-BT1001
    """

    product_code = request.args.get(
        "product_id",
        "",
    ).strip().upper()

    if not product_code:
        return render_template(
            "verify_product.html",
            error="Please enter a product code.",
        )

    product = get_product_from_database(product_code)

    if product is None:
        return render_template(
            "verify_product.html",
            error="Product not found or invalid product code.",
            entered_product_id=product_code,
        )

    return render_template(
        "product_details.html",
        product=product,
    )


@customer_bp.route("/verify/<product_code>")
def verify_by_qr(product_code):
    """
    This route opens when the customer scans the QR code.

    Example:
    /verify/BS-BT1001
    """

    product_code = product_code.strip().upper()

    product = get_product_from_database(product_code)

    if product is None:
        return render_template(
            "verify_product.html",
            error="This QR code does not match a registered product.",
            entered_product_id=product_code,
        )

    return render_template(
        "product_details.html",
        product=product,
    )


@customer_bp.route("/blockchain-history")
def blockchain_history():

    product_code = request.args.get(
        "product_id",
        "",
    ).strip().upper()

    if not product_code:
        return redirect(
            url_for("customer.verify_product")
        )

    db = Database()

    try:
        history = db.fetchall(
            """
            SELECT *
            FROM blockchain
            WHERE product_code = ?
            ORDER BY block_number ASC
            """,
            (product_code,),
        )

    finally:
        db.close()

    return render_template(
        "blockchain_history.html",
        product_id=product_code,
        history=history,
    )

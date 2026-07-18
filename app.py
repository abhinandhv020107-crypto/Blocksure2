from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/manufacturer")
def manufacturer_dashboard():
    return render_template("manufacturer_dashboard.html")


@app.route("/seller")
def seller_dashboard():
    return render_template("seller_dashboard.html")


@app.route("/customer")
def customer():
    return render_template("customer.html")


@app.route("/verify")
def verify_product():
    return render_template("verify_product.html")


@app.route("/add-product")
def add_product():
    return render_template("add_product.html")


@app.route("/product-details")
def product_details():
    return render_template("product_details.html")


@app.route("/blockchain-history")
def blockchain_history():
    return render_template("blockchain_history.html")


if __name__ == "__main__":
    app.run(debug=True)

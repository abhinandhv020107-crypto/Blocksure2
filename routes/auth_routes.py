from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("home.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "").strip().lower()
        if not email or not password or role not in {"admin", "manufacturer", "seller", "customer"}:
            flash("Please enter all login details.", "error")
            return render_template("login.html"), 400
        session["email"] = email
        session["role"] = role
        destinations = {
            "admin": "admin.dashboard",
            "manufacturer": "manufacturer.dashboard",
            "seller": "seller.dashboard",
            "customer": "customer.dashboard",
        }
        return redirect(url_for(destinations[role]))
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

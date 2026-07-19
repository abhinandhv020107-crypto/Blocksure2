from flask import Flask

from database.database import Database

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.manufacturer_routes import manufacturer_bp
from routes.seller_routes import seller_bp
from routes.customer_routes import customer_bp


app = Flask(__name__)

# Secret key for sessions
app.secret_key = "blocksure-secret-key-2026"

# Create database tables if they don't exist
db = Database()
db.create_tables()
db.close()

# Register all Blueprint routes
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(manufacturer_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(customer_bp)


# Optional home route
@app.route("/")
def home():
    return """
    <h2>Welcome to BlockSure</h2>
    <p><a href="/login">Go to Login</a></p>
    """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

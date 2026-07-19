from flask import Flask

from database.database import Database

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.manufacturer_routes import manufacturer_bp
from routes.seller_routes import seller_bp
from routes.customer_routes import customer_bp


app = Flask(__name__)

app.secret_key = "blocksure-secret-key-2026"


# Create database tables
database = Database()
database.create_tables()
database.close()


# Register all Blueprint routes
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(manufacturer_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(customer_bp)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )

from flask import Flask
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.manufacturer_routes import manufacturer_bp
from routes.seller_routes import seller_bp
from routes.customer_routes import customer_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "blocksure-development-key"
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(manufacturer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(customer_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

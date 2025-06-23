from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flasgger import Swagger


load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devsecret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Uplyft E-commerce API",
            "description": "API documentation for Uplyft E-commerce backend. JWT Bearer token required for protected endpoints.",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
            }
        },
    }
    Swagger(app, config=swagger_config, template=template)

    from backend.auth import auth_bp
    from backend.products import products_bp
    from backend.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    # Move CORS after blueprint registration
    CORS(
        app,
        supports_credentials=True,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers="*",
        methods=["GET", "POST", "OPTIONS"],
    )

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

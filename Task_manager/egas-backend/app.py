from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt, mail
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=[app.config["FRONTEND_URL"]])

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(employee_bp, url_prefix="/api")

    @app.route("/")
    def health_check():
        return {"status": "Backend is running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
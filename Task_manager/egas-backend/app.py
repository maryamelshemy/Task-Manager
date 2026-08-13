from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt, mail
from routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=[app.config["FRONTEND_URL"]])

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    from routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
   

    @app.route("/")
    def health_check():
        return {"status": "Backend is running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
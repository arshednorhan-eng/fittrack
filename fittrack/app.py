from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from pydantic import ValidationError

from fittrack.config import Config
from fittrack.database import db
from fittrack.exceptions import AppError, NotFoundError, DuplicateError, BusinessRuleError


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    from fittrack.routes.member_routes import bp as members_bp
    from fittrack.routes.subscription_routes import bp as subs_bp
    from fittrack.routes.class_routes import bp as classes_bp
    from fittrack.routes.workout_routes import bp as workouts_bp
    from fittrack.routes.checkin_routes import bp as checkin_bp

    app.register_blueprint(members_bp)
    app.register_blueprint(subs_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(checkin_bp)

    @app.get("/")
    def health():
        return {"status": "ok", "service": "FitTrack API"}

    # Error handlers
    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": "NotFoundError", "message": str(e)}), 404

    @app.errorhandler(DuplicateError)
    def handle_duplicate(e):
        return jsonify({"error": "DuplicateError", "message": str(e)}), 409

    @app.errorhandler(BusinessRuleError)
    def handle_business(e):
        return jsonify({"error": "BusinessRuleError", "message": str(e)}), 400

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": "ValidationError", "details": e.errors()}), 422

    @app.errorhandler(AppError)
    def handle_app_error(e):
        # fallback for custom domain errors
        status = getattr(e, "status_code", 400)
        return jsonify({"error": e.__class__.__name__, "message": str(e)}), status

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.name, "message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_generic(e):
        # Don't leak internal exceptions in production
        if app.debug:
            return jsonify({"error": "InternalServerError", "message": str(e)}), 500
        return jsonify({"error": "InternalServerError", "message": "Unexpected error occurred"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    # Optional: keep create_all only for quick dev.
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

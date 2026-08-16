import os
import logging
from flask import Flask, request
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )

    app.config.from_object(config[config_name])

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    logger.info(f"Application created with {config_name} configuration")

    from models import db
    db.init_app(app)

    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")

    _register_error_handlers(app)
    _register_blueprints(app)

    logger.info("Application initialized successfully")
    return app


def _register_blueprints(app):
    try:
        from app.routes import tasks_bp
        app.register_blueprint(tasks_bp)
        logger.info("Blueprints registered successfully")
    except ImportError as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise


def _register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 error: {request.path}")
        return {'error': 'Page not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        return {'error': 'Internal server error'}, 500

    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"400 error: {error}")
        return {'error': 'Bad request'}, 400

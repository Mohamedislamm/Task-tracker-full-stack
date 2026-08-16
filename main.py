import os
import sys
import logging
from app import create_app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_app():
    try:
        env = os.getenv('FLASK_ENV', 'development')
        app = create_app(env)
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = app.config.get('DEBUG', False)

        logger.info(f"Starting Task Tracker in {env} mode...")
        logger.info(f"Task Tracker running at http://{host}:{port}")

        app.run(host=host, port=port, debug=debug, use_reloader=debug)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    run_app()

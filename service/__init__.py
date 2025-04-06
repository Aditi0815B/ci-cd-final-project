"""
Service Package
"""
from flask import Flask

app = Flask(__name__)

# These imports must come after the Flask app is created
from service import routes
from service.common import log_handlers

# Initialize logging
log_handlers.init_logging(app, "gunicorn.error")

# Log startup banner
app.logger.info("*" * 70)
app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info("*" * 70)

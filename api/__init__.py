from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")
from .routes import *      # ✅ THIS loads app/api/routes.py
from .user import user
from .auth_route import *

api.register_blueprint(user)
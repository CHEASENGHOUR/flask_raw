from . import user
from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from config import Config
from db import get_db
from api.auth_route import require_jwt

@user.route("/", methods=["GET"])
@require_jwt
def user_home():
    return {
        "message": "Welcome to the user root"
    }
from config import Config
from flask import request, jsonify
from . import api
from db import get_db

import jwt, datetime, hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@api.route("/register", methods=["POST"])
def register():
    data = request.form if request.form else request.json

    if not data:
        return {"error": "Missing data"}, 400

    name = data.get("name")
    email = data.get("email")
    password_raw = data.get("password")

    if not password_raw:
        return {"error": "Password is required"}, 400

    password = hash_password(password_raw)

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    db.commit()

    return {"message": "User registered successfully"}



@api.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = hash_password(data.get("password"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                   (email, password))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


def require_jwt(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing token"}), 401

        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        try:
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


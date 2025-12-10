from . import user
from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from config import Config
from db import get_db
from api.auth_route import require_jwt

@user.route("/", methods=["GET"])
@require_jwt
def get_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    return jsonify(users)


@user.route("/<int:id>", methods=["GET"])
@require_jwt
def get_user(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id=%s", (id,))
    users = cursor.fetchone()
    return jsonify(users)

@user.route("/<int:id>", methods=["PUT"])
@require_jwt
def update_user(id):
    name = request.form.get("name")
    email = request.form.get("email")
    image = request.files.get("image")

    filename = None
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(Config.UPLOAD_FOLDER, filename))

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET name=%s, email=%s, image=%s WHERE id=%s",
        (name, email, filename, id)
    )
    db.commit()

    return jsonify({"message": "User updated"})

@user.route("/<int:id>", methods=["DELETE"])
@require_jwt
def delete_user(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()

    return jsonify({"message": "User deleted"})
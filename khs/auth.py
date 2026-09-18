import jwt, bcrypt, os
from flask import Blueprint, request, jsonify
from db import users

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    data["password"] = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
    users.insert_one(data)
    return jsonify({"msg": "Registered"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})
    if not user or not bcrypt.checkpw(data["password"].encode(), user["password"]):
        return jsonify({"error": "Invalid"}), 401

    token = jwt.encode({"email": user["email"]}, os.getenv("JWT_SECRET"), algorithm="HS256")
    return jsonify({"token": token})

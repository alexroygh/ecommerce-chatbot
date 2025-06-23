from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
            required:
              - username
              - password
    responses:
      201:
        description: User registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
      400:
        description: Missing username or password
      409:
        description: Username already exists
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User login
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
            required:
              - username
              - password
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

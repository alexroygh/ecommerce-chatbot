from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Product
import datetime
from flask_cors import cross_origin

chat_bp = Blueprint("chat", __name__)

chat_history = {}


@chat_bp.route("", methods=["POST"])
@chat_bp.route("/", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@jwt_required()
def chat():
    try:
        data = request.get_json(force=True)
        if not data or "message" not in data:
            return jsonify({"msg": "Missing or invalid JSON body"}), 400
        user_id = get_jwt_identity()
        message = data.get("message")
        timestamp = datetime.datetime.utcnow().isoformat()

        response = {
            "reply": "I'm a sales bot! Please ask about products or categories.",
            "timestamp": timestamp,
        }
        if message:
            products = Product.query.filter(Product.name.ilike(f"%{message}%")).all()
            if products:
                response["reply"] = f"Found {len(products)} product(s): " + ", ".join(
                    [p.name for p in products]
                )
            else:
                response["reply"] = (
                    "Sorry, I couldn't find any products matching your query."
                )

        if user_id not in chat_history:
            chat_history[user_id] = []
        chat_history[user_id].append(
            {"message": message, "response": response["reply"], "timestamp": timestamp}
        )

        return jsonify(response)

    except Exception as e:
        print("Chat route error:", str(e))
        return jsonify({"msg": "Something went wrong"}), 500

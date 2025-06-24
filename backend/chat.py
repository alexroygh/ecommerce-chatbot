from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Product, ChatMessage
from backend.app import db
import datetime
from flask_cors import cross_origin
import re
import json

chat_bp = Blueprint("chat", __name__)


def search_by_id(message):
    number_match = re.search(r"\b(\d+)\b", message)
    if number_match:
        product = Product.query.get(int(number_match.group(1)))
        if product:
            return [product]
    return []


def search_by_product_name(message):
    prod_name_match = re.search(r"product\s*(\d+)", message, re.IGNORECASE)
    if prod_name_match:
        prod_name = f"Product {prod_name_match.group(1)}"
        return Product.query.filter(Product.name.ilike(f"%{prod_name}%")).all()
    return []


def search_by_name_words(message):
    words = [w for w in re.split(r"\W+", message) if w]
    products = []
    for word in words:
        found = Product.query.filter(Product.name.ilike(f"%{word}%")).all()
        products.extend(found)
    # Remove duplicates
    return list({p.id: p for p in products}.values())


def search_by_category(message):
    words = [w for w in re.split(r"\W+", message) if w]
    categories = [
        c[0] for c in Product.query.with_entities(Product.category).distinct().all()
    ]
    for word in words:
        for category in categories:
            if word.lower() == category.lower():
                return Product.query.filter_by(category=category).all()
    return []


@chat_bp.route("", methods=["POST"])
@cross_origin(origins="*", supports_credentials=True)
@jwt_required()
def chat():
    """
    Chat with the sales bot
    ---
    tags:
      - Chat
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
            required:
              - message
    responses:
      200:
        description: Bot reply and updated chat history
        content:
          application/json:
            schema:
              type: object
              properties:
                reply:
                  type: string
                products:
                  type: array
                  items:
                    type: object
                    properties:
                      id: { type: integer }
                      name: { type: string }
                      price: { type: number }
                      category: { type: string }
                      description: { type: string }
                      image_url: { type: string }
                      stock: { type: integer }
                timestamp:
                  type: string
                history:
                  type: array
                  items:
                    type: object
                    properties:
                      sender: { type: string }
                      message: { type: string }
                      products:
                        type: array
                        items:
                          type: object
                          properties:
                            id: { type: integer }
                            name: { type: string }
                            price: { type: number }
                            category: { type: string }
                            description: { type: string }
                            image_url: { type: string }
                            stock: { type: integer }
                      timestamp: { type: string }
      400:
        description: Missing or invalid JSON body
      500:
        description: Something went wrong
    """
    try:
        data = request.get_json(force=True)
        if not data or "message" not in data:
            return (
                jsonify(
                    {
                        "reply": "Missing or invalid JSON body",
                        "products": [],
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "history": [],
                    }
                ),
                400,
            )

        user_id = get_jwt_identity()
        message = data.get("message")
        timestamp = datetime.datetime.utcnow()

        products = (
            search_by_id(message)
            or search_by_product_name(message)
            or search_by_name_words(message)
            or search_by_category(message)
        )

        if products:
            reply = f"Found {len(products)} product(s)."
        else:
            reply = "Sorry, I couldn't find any products matching your query."

        # Store user message (plain text)
        db.session.add(
            ChatMessage(
                user_id=user_id, sender="user", message=message, timestamp=timestamp
            )
        )
        # Store bot message (full response as JSON string)
        bot_message_json = json.dumps(
            {
                "reply": reply,
                "products": (
                    [
                        {
                            "id": p.id,
                            "name": p.name,
                            "price": p.price,
                            "category": p.category,
                            "description": p.description,
                            "image_url": p.image_url,
                            "stock": p.stock,
                        }
                        for p in products
                    ]
                    if products
                    else []
                ),
                "timestamp": timestamp.isoformat(),
            }
        )
        db.session.add(
            ChatMessage(
                user_id=user_id,
                sender="bot",
                message=bot_message_json,
                timestamp=timestamp,
            )
        )
        db.session.commit()

        # Retrieve chat history for the user, ordered by timestamp
        history = (
            ChatMessage.query.filter_by(user_id=str(user_id))
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )
        history_serialized = []
        for m in history:
            if m.sender == "bot":
                try:
                    bot_data = json.loads(m.message)
                    history_serialized.append(
                        {
                            "sender": "bot",
                            "message": bot_data.get("reply", ""),
                            "products": bot_data.get("products", []),
                            "timestamp": bot_data.get(
                                "timestamp", m.timestamp.isoformat()
                            ),
                        }
                    )
                except Exception:
                    history_serialized.append(
                        {
                            "sender": "bot",
                            "message": m.message,
                            "products": [],
                            "timestamp": m.timestamp.isoformat(),
                        }
                    )
            else:
                history_serialized.append(
                    {
                        "sender": "user",
                        "message": m.message,
                        "timestamp": m.timestamp.isoformat(),
                    }
                )

        return jsonify(
            {
                "reply": reply,
                "products": (
                    [
                        {
                            "id": p.id,
                            "name": p.name,
                            "price": p.price,
                            "category": p.category,
                            "description": p.description,
                            "image_url": p.image_url,
                            "stock": p.stock,
                        }
                        for p in products
                    ]
                    if products
                    else []
                ),
                "timestamp": timestamp.isoformat(),
                "history": history_serialized,
            }
        )

    except Exception as e:
        print("Chat route error:", str(e))
        return (
            jsonify(
                {
                    "reply": "Something went wrong",
                    "products": [],
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "history": [],
                }
            ),
            500,
        )

@chat_bp.route("", methods=["GET"])
@cross_origin(origins="*", supports_credentials=True)
@jwt_required()
def get_chat_history():
    """
    Get all chat messages for the current user (user and bot), ordered by timestamp.
    ---
    tags:
      - Chat
    security:
      - BearerAuth: []
    responses:
      200:
        description: All chat messages for the user
        content:
          application/json:
            schema:
              type: object
              properties:
                history:
                  type: array
                  items:
                    type: object
                    properties:
                      sender: { type: string }
                      message: { type: string }
                      products:
                        type: array
                        items:
                          type: object
                          properties:
                            id: { type: integer }
                            name: { type: string }
                            price: { type: number }
                            category: { type: string }
                            description: { type: string }
                            image_url: { type: string }
                            stock: { type: integer }
                      timestamp: { type: string }
      500:
        description: Something went wrong
    """
    try:
        user_id = get_jwt_identity()
        # Fetch all messages for this user, ordered by timestamp
        history = (
            ChatMessage.query.filter_by(user_id=str(user_id))
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )
        history_serialized = []
        for m in history:
            if m.sender == "bot":
                try:
                    bot_data = json.loads(m.message)
                    history_serialized.append(
                        {
                            "sender": "bot",
                            "message": bot_data.get("reply", ""),
                            "products": bot_data.get("products", []),
                            "timestamp": bot_data.get(
                                "timestamp", m.timestamp.isoformat()
                            ),
                        }
                    )
                except Exception:
                    history_serialized.append(
                        {
                            "sender": "bot",
                            "message": m.message,
                            "products": [],
                            "timestamp": m.timestamp.isoformat(),
                        }
                    )
            else:
                history_serialized.append(
                    {
                        "sender": "user",
                        "message": m.message,
                        "timestamp": m.timestamp.isoformat(),
                    }
                )
        return jsonify({"history": history_serialized}), 200
    except Exception as e:
        print("Get chat history error:", str(e))
        return jsonify({"history": [], "error": "Something went wrong"}), 500

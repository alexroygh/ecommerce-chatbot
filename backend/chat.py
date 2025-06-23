from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Product
import datetime
from flask_cors import cross_origin
import re

chat_bp = Blueprint("chat", __name__)

chat_history = {}


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
@chat_bp.route("/", methods=["POST"])
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
        description: Bot reply
        content:
          application/json:
            schema:
              type: object
              properties:
                reply:
                  type: string
                timestamp:
                  type: string
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
                    }
                ),
                400,
            )

        user_id = get_jwt_identity()
        message = data.get("message")
        timestamp = datetime.datetime.utcnow().isoformat()

        products = (
            search_by_id(message)
            or search_by_product_name(message)
            or search_by_name_words(message)
            or search_by_category(message)
        )

        if products:
            return jsonify(
                {
                    "reply": f"Found {len(products)} product(s).",
                    "products": [
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
                    ],
                    "timestamp": timestamp,
                }
            )
        else:
            return jsonify(
                {
                    "reply": "Sorry, I couldn't find any products matching your query.",
                    "products": [],
                    "timestamp": timestamp,
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
                }
            ),
            500,
        )

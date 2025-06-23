from flask import Blueprint, request, jsonify
from backend.models import Product

products_bp = Blueprint("products", __name__)


@products_bp.route("/", methods=["GET"])
def list_products():
    query = Product.query
    search = request.args.get("search")
    category = request.args.get("category")
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter_by(category=category)
    products = query.all()
    return jsonify(
        [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "category": p.category,
                "image_url": p.image_url,
                "stock": p.stock,
            }
            for p in products
        ]
    )

@products_bp.route("/<int:product_id>/", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "image_url": product.image_url,
        "stock": product.stock,
    })

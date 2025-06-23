from flask import Blueprint, request, jsonify
from backend.models import Product

products_bp = Blueprint("products", __name__)


@products_bp.route("/", methods=["GET"])
def list_products():
    """
    List all products or search by name/category
    ---
    tags:
      - Products
    parameters:
      - name: search
        in: query
        type: string
        description: Search term for product name
      - name: category
        in: query
        type: string
        description: Filter by category
    responses:
      200:
        description: List of products
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
                  price:
                    type: number
                  category:
                    type: string
                  image_url:
                    type: string
                  stock:
                    type: integer
    """
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
    """
    Get product details by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID of the product
    responses:
      200:
        description: Product details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                price:
                  type: number
                category:
                  type: string
                image_url:
                  type: string
                stock:
                  type: integer
      404:
        description: Product not found
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "image_url": product.image_url,
            "stock": product.stock,
        }
    )

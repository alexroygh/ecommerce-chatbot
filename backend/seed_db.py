from backend.app import create_app, db
from backend.models import Product, User
import random


def seed():
    app = create_app()
    with app.app_context():
        # Add test users
        if not User.query.filter_by(username="test1").first():
            user1 = User(username="test1")
            user1.set_password("test123")
            db.session.add(user1)
        if not User.query.filter_by(username="test2").first():
            user2 = User(username="test2")
            user2.set_password("test123")
            db.session.add(user2)
        db.session.commit()

        if Product.query.count() == 0:
            categories = [
                "Electronics",
                "Books",
                "Clothing",
                "Toys",
                "Home & Kitchen",
                "Sports",
                "Beauty",
                "Garden",
            ]
            product_data = [
                {
                    "name": "Apple iPhone 14",
                    "category": "Electronics",
                    "description": "The latest iPhone with advanced camera and display.",
                    "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Samsung Galaxy S23",
                    "category": "Electronics",
                    "description": "Flagship Android smartphone with high performance.",
                    "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Sony WH-1000XM5 Headphones",
                    "category": "Electronics",
                    "description": "Industry-leading noise cancelling headphones.",
                    "image_url": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "The Great Gatsby",
                    "category": "Books",
                    "description": "Classic novel by F. Scott Fitzgerald.",
                    "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Nike Air Max 270",
                    "category": "Clothing",
                    "description": "Comfortable and stylish sneakers for everyday wear.",
                    "image_url": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "LEGO Star Wars Set",
                    "category": "Toys",
                    "description": "Build your own Star Wars adventure with LEGO.",
                    "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Instant Pot Duo 7-in-1",
                    "category": "Home & Kitchen",
                    "description": "Versatile multi-cooker for fast, easy meals.",
                    "image_url": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Wilson Tennis Racket",
                    "category": "Sports",
                    "description": "Lightweight racket for all skill levels.",
                    "image_url": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Maybelline Mascara",
                    "category": "Beauty",
                    "description": "Volumizing mascara for bold lashes.",
                    "image_url": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80",
                },
                {
                    "name": "Weber Charcoal Grill",
                    "category": "Garden",
                    "description": "Classic charcoal grill for outdoor cooking.",
                    "image_url": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80",
                },
            ]
            for i in range(1, 51):
                prod = random.choice(product_data)
                p = Product(
                    name=prod["name"],
                    description=prod["description"],
                    price=round(random.uniform(10, 1000), 2),
                    category=prod["category"],
                    image_url=prod["image_url"],
                    stock=random.randint(1, 100),
                )
                db.session.add(p)
            db.session.commit()
            print("Seeded 50 realistic products.")
        else:
            print("Products already seeded.")


if __name__ == "__main__":
    seed()

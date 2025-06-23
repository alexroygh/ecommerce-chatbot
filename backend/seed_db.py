from app import create_app, db
from models import Product
import random


def seed():
    app = create_app()
    with app.app_context():
        if Product.query.count() == 0:
            categories = ["Electronics", "Books", "Textiles", "Toys", "Home", "Sports"]
            for i in range(1, 101):
                p = Product(
                    name=f"Product {i}",
                    description=f"Description for product {i}",
                    price=round(random.uniform(10, 500), 2),
                    category=random.choice(categories),
                    image_url=f"https://via.placeholder.com/150?text=Product+{i}",
                    stock=random.randint(1, 100),
                )
                db.session.add(p)
            db.session.commit()
            print("Seeded 100 products.")
        else:
            print("Products already seeded.")


if __name__ == "__main__":
    seed()

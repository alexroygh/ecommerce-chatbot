from app import create_app, db
from models import Product
import random

CATEGORIES = ['Electronics', 'Books', 'Textiles', 'Toys', 'Home', 'Sports']
PRODUCTS = [
    {
        'name': f'Product {i}',
        'description': f'Description for product {i}',
        'price': round(random.uniform(10, 500), 2),
        'category': random.choice(CATEGORIES),
        'image_url': f'https://via.placeholder.com/150?text=Product+{i}',
        'stock': random.randint(1, 100)
    }
    for i in range(1, 101)
]

def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        for prod in PRODUCTS:
            p = Product(**prod)
            db.session.add(p)
        db.session.commit()
        print('Database initialized with 100 products.')

if __name__ == '__main__':
    main() 
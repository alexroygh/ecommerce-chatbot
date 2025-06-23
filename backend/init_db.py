from backend.app import create_app, db
from backend.models import Product


def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print("Database initialized")


if __name__ == "__main__":
    main()

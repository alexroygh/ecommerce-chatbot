# Backend - E-commerce Chatbot

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Migrations (Flask-Migrate):**
   - Initialize migrations (first time only):
     ```bash
     flask db init
     ```
   - Generate a migration after model changes:
     ```bash
     flask db migrate -m "Initial migration."
     ```
   - Apply migrations:
     ```bash
     flask db upgrade
     ```
4. **Seed the database with mock products:**
   ```bash
   python seed_db.py
   ```
5. Run the server:
   ```bash
   flask run
   ```

## API Endpoints
- `/api/auth/login` - User login
- `/api/auth/register` - User registration
- `/api/chat` - Chatbot endpoint
- `/api/products` - Product search/listing

## Database
- SQLite (via SQLAlchemy)
- Managed with Flask-Migrate (Alembic)
- Seeded with 100+ mock products using `seed_db.py`

## Running Backend Tests

To run the backend tests, make sure you have installed the requirements:

```bash
pip install -r requirements.txt
```

Then run:

```bash
pytest
```

This will automatically discover and run all tests in the backend directory.

## Running Tests with Coverage

To run the backend tests and see a coverage report, use:

```bash
pytest --cov=.
```

This will show a summary in the terminal. For an HTML report:

```bash
pytest --cov=. --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view it.

---

## Troubleshooting

### Error: `
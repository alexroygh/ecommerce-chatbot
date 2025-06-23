# Backend - Uplyft E-commerce Chatbot

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

---

## Troubleshooting

### Error: `no such table: user`
This means the database tables have not been created. **Run migrations:**
```bash
flask db upgrade
```
Then seed the database and restart your Flask server.

See `project_report.md` for architecture and design notes. 
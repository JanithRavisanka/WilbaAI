# WilbaAI FastAPI Boilerplate

## Features

- Modular FastAPI structure
- MySQL with SQLAlchemy ORM
- Pydantic settings via `.env`
- Context-managed DB sessions
- Sample endpoints for all modules

## Running

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your `.env` file with MySQL credentials.

3. Run migrations (manual for now, or use Alembic).

4. Start the app:
   ```
   uvicorn app.main:app --reload
   ```

## Database Migrations with Alembic

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations, similar to Django migrations.

### How to Use Alembic

1. **Install Alembic and MySQL driver:**
   ```
   pip install alembic pymysql
   ```
2. **Configure your database URL** in `alembic.ini` (already set for MySQL):
   ```ini
   sqlalchemy.url = mysql+pymysql://root:root@localhost:3306/wilbaai
   ```
3. **Generate a migration:**
   ```
   alembic revision --autogenerate -m "Your migration message"
   ```
4. **Apply migrations:**
   ```
   alembic upgrade head
   ```

**Troubleshooting:**
If you get `ModuleNotFoundError: No module named 'pymysql'` or similar errors, make sure you are running Alembic from your virtual environment:

```
source .venv/bin/activate
alembic revision --autogenerate -m "Your migration message"
```

See the [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/) for more details.

## Project Structure

(see code for details)
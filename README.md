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

## Project Structure

(see code for details)
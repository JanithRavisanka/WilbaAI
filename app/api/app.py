from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.app_models import AppRead

router = APIRouter(prefix="/app", tags=["app"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AppRead])
def list_apps(db: Session = Depends(get_db)):
    # Dummy response for boilerplate
    return []
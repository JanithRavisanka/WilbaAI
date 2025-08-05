from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.app_entity import App as AppModel
from app.models.app_models import AppRead, AppCreate

router = APIRouter(prefix="/app", tags=["app"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AppRead])
def list_apps(db: Session = Depends(get_db)):
    return db.query(AppModel).all()

@router.post("/", response_model=AppRead, status_code=status.HTTP_201_CREATED)
def create_app(app: AppCreate, db: Session = Depends(get_db)):
    db_app = AppModel(name=app.name)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@router.get("/{app_id}", response_model=AppRead)
def get_app(app_id: int, db: Session = Depends(get_db)):
    app = db.query(AppModel).filter(AppModel.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return app

@router.put("/{app_id}", response_model=AppRead)
def update_app(app_id: int, app_update: AppCreate, db: Session = Depends(get_db)):
    app = db.query(AppModel).filter(AppModel.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    app.name = app_update.name
    db.commit()
    db.refresh(app)
    return app

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_app(app_id: int, db: Session = Depends(get_db)):
    app = db.query(AppModel).filter(AppModel.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    db.delete(app)
    db.commit()
    return None
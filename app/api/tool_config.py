from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.tool_entity import ToolConfig as ToolConfigModel
from app.models.tool_models import ToolConfigRead, ToolConfigCreate

router = APIRouter(prefix="/tool-config", tags=["tool-config"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/app/{app_id}", response_model=ToolConfigRead)
def get_tool_config_by_app_id(app_id: int, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig for this app not found")
    return config

@router.post("/", response_model=ToolConfigRead, status_code=status.HTTP_201_CREATED)
def create_tool_config(tool_config: ToolConfigCreate, db: Session = Depends(get_db)):
    # Enforce one-to-one: only one ToolConfig per app
    existing = db.query(ToolConfigModel).filter(ToolConfigModel.app_id == tool_config.app_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ToolConfig for this app already exists")
    db_config = ToolConfigModel(config=tool_config.config, app_id=tool_config.app_id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.put("/app/{app_id}", response_model=ToolConfigRead)
def update_tool_config_by_app_id(app_id: int, tool_config: ToolConfigCreate, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig for this app not found")
    config.config = tool_config.config
    db.commit()
    db.refresh(config)
    return config

@router.delete("/app/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool_config_by_app_id(app_id: int, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig for this app not found")
    db.delete(config)
    db.commit()
    return None
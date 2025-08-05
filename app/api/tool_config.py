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

@router.get("/", response_model=list[ToolConfigRead])
def list_tool_configs(db: Session = Depends(get_db)):
    configs = db.query(ToolConfigModel).all()
    return configs

@router.post("/", response_model=ToolConfigRead, status_code=status.HTTP_201_CREATED)
def create_tool_config(tool_config: ToolConfigCreate, db: Session = Depends(get_db)):
    db_config = ToolConfigModel(config=tool_config.config)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/{config_id}", response_model=ToolConfigRead)
def get_tool_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig not found")
    return config

@router.put("/{config_id}", response_model=ToolConfigRead)
def update_tool_config(config_id: int, tool_config: ToolConfigCreate, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig not found")
    config.config = tool_config.config
    db.commit()
    db.refresh(config)
    return config

@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(ToolConfigModel).filter(ToolConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="ToolConfig not found")
    db.delete(config)
    db.commit()
    return None
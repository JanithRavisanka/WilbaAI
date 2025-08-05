from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.agent_entity import AgentConfig as AgentConfigModel
from app.models.agent_models import AgentConfigRead, AgentConfigCreate

router = APIRouter(prefix="/agent-config", tags=["agent-config"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/app/{app_id}", response_model=AgentConfigRead)
def get_agent_config_by_app_id(app_id: int, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig for this app not found")
    return config

@router.post("/", response_model=AgentConfigRead, status_code=status.HTTP_201_CREATED)
def create_agent_config(agent_config: AgentConfigCreate, db: Session = Depends(get_db)):
    # Enforce one-to-one: only one AgentConfig per app
    existing = db.query(AgentConfigModel).filter(AgentConfigModel.app_id == agent_config.app_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="AgentConfig for this app already exists")
    db_config = AgentConfigModel(config=agent_config.config, app_id=agent_config.app_id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.put("/app/{app_id}", response_model=AgentConfigRead)
def update_agent_config_by_app_id(app_id: int, agent_config: AgentConfigCreate, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig for this app not found")
    config.config = agent_config.config
    db.commit()
    db.refresh(config)
    return config

@router.delete("/app/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent_config_by_app_id(app_id: int, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.app_id == app_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig for this app not found")
    db.delete(config)
    db.commit()
    return None
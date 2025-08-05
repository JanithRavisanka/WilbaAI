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

@router.get("/", response_model=list[AgentConfigRead])
def list_agent_configs(db: Session = Depends(get_db)):
    configs = db.query(AgentConfigModel).all()
    return configs

@router.post("/", response_model=AgentConfigRead, status_code=status.HTTP_201_CREATED)
def create_agent_config(agent_config: AgentConfigCreate, db: Session = Depends(get_db)):
    db_config = AgentConfigModel(config=agent_config.config)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/{config_id}", response_model=AgentConfigRead)
def get_agent_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig not found")
    return config

@router.put("/{config_id}", response_model=AgentConfigRead)
def update_agent_config(config_id: int, agent_config: AgentConfigCreate, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig not found")
    config.config = agent_config.config
    db.commit()
    db.refresh(config)
    return config

@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(AgentConfigModel).filter(AgentConfigModel.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="AgentConfig not found")
    db.delete(config)
    db.commit()
    return None
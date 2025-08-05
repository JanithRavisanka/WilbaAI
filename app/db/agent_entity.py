from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class AgentConfig(Base):
    __tablename__ = "agent_configs"
    id = Column(Integer, primary_key=True, index=True)
    config = Column(String(255))
    app_id = Column(Integer, ForeignKey("apps.id"))
    app = relationship("App", back_populates="agent_config")
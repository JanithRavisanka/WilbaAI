from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class App(Base):
    __tablename__ = "apps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    agent_config = relationship("AgentConfig", uselist=False, back_populates="app")
    tool_config = relationship("ToolConfig", uselist=False, back_populates="app")
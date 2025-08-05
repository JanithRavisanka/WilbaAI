from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class ToolConfig(Base):
    __tablename__ = "tool_configs"
    id = Column(Integer, primary_key=True, index=True)
    config = Column(String(255))
    app_id = Column(Integer, ForeignKey("apps.id"))
    app = relationship("App", back_populates="tool_config")
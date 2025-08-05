from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class System(Base):
    __tablename__ = "systems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    apps = relationship("App", backref="system")
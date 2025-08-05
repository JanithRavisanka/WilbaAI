from app.db.base import Base
from app.db.session import engine
import app.db.app_entity
import app.db.agent_entity
import app.db.tool_entity
import app.db.system_entity

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
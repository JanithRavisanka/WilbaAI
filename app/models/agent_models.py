from pydantic import BaseModel

class AgentConfigBase(BaseModel):
    config: str

class AgentConfigCreate(AgentConfigBase):
    pass

class AgentConfigRead(AgentConfigBase):
    id: int
    class Config:
        from_attributes = True
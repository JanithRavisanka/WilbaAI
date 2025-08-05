from pydantic import BaseModel

class ToolConfigBase(BaseModel):
    config: str

class ToolConfigCreate(ToolConfigBase):
    pass

class ToolConfigRead(ToolConfigBase):
    id: int
    class Config:
        from_attributes = True
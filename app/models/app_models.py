from pydantic import BaseModel

class AppBase(BaseModel):
    name: str

class AppCreate(AppBase):
    pass

class AppRead(AppBase):
    id: int
    class Config:
        from_attributes = True
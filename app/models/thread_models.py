from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ThreadBase(BaseModel):
    title: str
    app_id: int

class ThreadCreate(ThreadBase):
    pass

class ThreadRead(ThreadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 
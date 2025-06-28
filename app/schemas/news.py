from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime
class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Union[str, None] = None
    published_at: Optional[datetime] = None

class NewsCreate(NewsBase):
    pass

class NewsUpdate(NewsBase):
    pass

class NewsOut(NewsBase):
    id: int

    class Config:
        orm_mode = True
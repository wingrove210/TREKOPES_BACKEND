from pydantic import BaseModel
from typing import Union
class TrackBase(BaseModel):
    title: str
    artist: str
    file_url: Union[str, None] = None
    image_url: Union[str, None] = None

class TrackCreate(TrackBase):
    pass

class TrackUpdate(TrackBase):
    pass

class TrackOut(TrackBase):
    id: int

    class Config:
        orm_mode = True
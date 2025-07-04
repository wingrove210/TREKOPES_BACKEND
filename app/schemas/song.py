from pydantic import BaseModel

class SongRequest(BaseModel):
    telegramChatId: str
    prompt: str
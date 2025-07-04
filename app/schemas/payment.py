from pydantic import BaseModel

class PaymentRequest(BaseModel):
    telegramChatId: str
    pack_id: int
    is_recurring: bool = False
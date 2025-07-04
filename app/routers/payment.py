from fastapi import APIRouter, HTTPException
import httpx
from core.config import settings
from schemas.payment import PaymentRequest

router = APIRouter()

@router.post("/process-payment")
async def process_payment(request: PaymentRequest):
    url = f"{settings.API_BASE_URL}/api/chats/{request.telegramChatId}/payments"
    payload = {
        "pack_id": request.pack_id,
        "is_recurring": request.is_recurring
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {settings.BEARER_TOKEN}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
# 0197c59e-2a53-7090-b881-e0ac2b288429
@router.get("/get-payment/{telegramChatId}/{payment_id}")
async def get_payment(telegramChatId: str, payment_id: int):
    url = f"{settings.API_BASE_URL}/api/chats/{telegramChatId}/payments/{payment_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"Authorization": f"Bearer {settings.BEARER_TOKEN}"}
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Payment not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

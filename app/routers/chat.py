from fastapi import APIRouter, HTTPException
import httpx
from core.config import settings

router = APIRouter(tags=["Чаты"])

@router.get("/get-chat/{telegramChatId}")
async def get_chat(telegramChatId: str):
    url = f"{settings.API_BASE_URL}/api/chats/{telegramChatId}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"Authorization": f"Bearer {settings.BEARER_TOKEN}"}
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Chat not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
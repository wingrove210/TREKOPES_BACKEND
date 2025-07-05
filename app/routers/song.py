from fastapi import APIRouter, HTTPException
import httpx
from core.config import settings
from schemas.song import SongRequest

router = APIRouter(tags=["Песни пользователя"])

@router.post("/generate-song")
async def generate_song(request: SongRequest):
    url = f"{settings.API_BASE_URL}/api/chats/{request.telegramChatId}/songs/generate"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"prompt": request.prompt},
            headers={"Authorization": f"Bearer {settings.BEARER_TOKEN}"}
        )
        print(response.url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    
    
@router.get("/get-song/{telegramChatId}/{song_id}")
async def get_song(telegramChatId: str, song_id: str):
    url = f"{settings.API_BASE_URL}/api/chats/{telegramChatId}/songs/{song_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"Authorization": f"Bearer {settings.BEARER_TOKEN}"}
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Song not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
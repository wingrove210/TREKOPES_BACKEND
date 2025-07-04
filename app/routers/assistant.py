#!/usr/bin/env python3

from __future__ import annotations
import datetime
from pydantic import BaseModel
from yandex_cloud_ml_sdk import YCloudML
from core.config import settings
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/assistant")

sdk = YCloudML(
        folder_id=settings.YCL_FOLDER_ID,
        auth=settings.YCL_SECRET_KEY,
    )
messages = [
    {
        "role": "system",
        "text": "Ты обкуренный алкаш, который хорошо знапет математику. Ты очень азартный.",
    },
    {
        "role": "user",
        "text": "",
    },
]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)



manager = ConnectionManager()

async def generate(text: str):
    messages[1]["text"] = text
    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)
    )
    
    message = ""
    for alternative in result:
        message = alternative.text
    return message

class Messages(BaseModel):
    text: str
    personal: bool
    timestamp: datetime.datetime

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            text = await generate(data)
            await manager.broadcast(f"{text}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
        



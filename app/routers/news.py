from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from crud import news as crud_news
from services.storage import S3Storage
from schemas.news import NewsCreate, NewsUpdate, NewsOut
from datetime import date

router = APIRouter(
    prefix="/news",
    tags=["Новости"]
)
@router.get("/", response_model=List[NewsOut])
async def read_news(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    news_items = await crud_news.get_news(db, skip=skip, limit=limit)
    return news_items

@router.get("/{news_id}", response_model=NewsOut)
async def read_news_item(news_id: int, db: AsyncSession = Depends(get_async_session)):
    db_news = await crud_news.get_news_item(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News item not found")
    return db_news

@router.post("/", response_model=NewsOut)
async def create_news_with_photo(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    storage: S3Storage = Depends(S3Storage)
):
    # Читаем и сохраняем изображение
    image_content = await image.read()
    storage.save(image.filename, image_content)
    image_url = storage.get(image.filename)

    news_in = NewsCreate(
        title=title,
        content=content,
        image_url=image_url,
        published_at=date.today()  # Текущая дата без времени
    )
    return await crud_news.create_news(db, news_in)

@router.put("/{news_id}", response_model=NewsOut)
async def update_news(news_id: int, news_in: NewsUpdate, db: AsyncSession = Depends(get_async_session)):
    db_news = await crud_news.update_news(db, news_id=news_id, news_in=news_in)
    if db_news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News item not found")
    return db_news

@router.delete("/{news_id}", response_model=NewsOut)
async def delete_news(news_id: int, db: AsyncSession = Depends(get_async_session)):
    db_news = await crud_news.delete_news(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News item not found")
    return db_news
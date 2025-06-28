from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News
from schemas.news import NewsCreate, NewsUpdate

async def get_news(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(News).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
async def get_news_item(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
async def create_news(db: AsyncSession, news_in: NewsCreate):
    db_news = News(**news_in.dict(exclude_unset=True))
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news
async def update_news(db: AsyncSession, news_id: int, news_in: NewsUpdate): 
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    db_news = result.scalar_one_or_none()
    if not db_news:
        return None
    for field, value in news_in.dict(exclude_unset=True).items():
        setattr(db_news, field, value)
    await db.commit()
    await db.refresh(db_news)
    return db_news
async def delete_news(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    db_news = result.scalar_one_or_none()
    if not db_news:
        return None
    await db.delete(db_news)
    await db.commit()
    return db_news
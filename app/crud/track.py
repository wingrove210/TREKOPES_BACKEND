from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.track import Track
from schemas.track import TrackCreate, TrackUpdate

async def get_tracks(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Track).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_track(db: AsyncSession, track_id: int):
    stmt = select(Track).where(Track.id == track_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_track(db: AsyncSession, track_in: TrackCreate):
    db_track = Track(**track_in.dict(exclude_unset=True))
    db.add(db_track)
    await db.commit()
    await db.refresh(db_track)
    return db_track

async def update_track(db: AsyncSession, track_id: int, track_in: TrackUpdate):
    stmt = select(Track).where(Track.id == track_id)
    result = await db.execute(stmt)
    db_track = result.scalar_one_or_none()
    if not db_track:
        return None
    for field, value in track_in.dict(exclude_unset=True).items():
        setattr(db_track, field, value)
    await db.commit()
    await db.refresh(db_track)
    return db_track

async def delete_track(db: AsyncSession, track_id: int):
    stmt = select(Track).where(Track.id == track_id)
    result = await db.execute(stmt)
    db_track = result.scalar_one_or_none()
    if not db_track:
        return None
    await db.delete(db_track)
    await db.commit()
    return db_track
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from crud import track as crud_track
from schemas.track import TrackBase, TrackCreate, TrackUpdate, TrackOut
from services.storage import S3Storage

router = APIRouter(
    prefix="/tracks",
    tags=["Треки"]
)

@router.get("/", response_model=List[TrackOut])
async def read_tracks(db: AsyncSession = Depends(get_async_session)):
    tracks = await crud_track.get_tracks(db)
    return tracks

@router.get("/{track_id}", response_model=TrackBase)
async def read_track(track_id: int, db: AsyncSession = Depends(get_async_session)):
    db_track = await crud_track.get_track(db, track_id=track_id)
    if db_track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return db_track

@router.post("/", response_model=TrackOut)
async def create_track_with_files(
    title: str = Form(...),
    artist: str = Form(...),
    file: UploadFile = File(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    storage: S3Storage = Depends(S3Storage)
):
    # Читаем и сохраняем трек
    file_content = await file.read()
    storage.save(file.filename, file_content)
    file_url = storage.get(file.filename)

    # Читаем и сохраняем изображение
    image_content = await image.read()
    storage.save(image.filename, image_content)
    image_url = storage.get(image.filename)

    track_in = TrackCreate(
        title=title,
        artist=artist,
        file_url=file_url,
        image_url=image_url
    )
    return await crud_track.create_track(db, track_in)

@router.put("/{track_id}", response_model=TrackBase)
async def update_track(track_id: int, track_in: TrackUpdate, db: AsyncSession = Depends(get_async_session)):
    db_track = await crud_track.update_track(db, track_id=track_id, track_in=track_in)
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return db_track

@router.delete("/{track_id}", response_model=TrackOut)
async def delete_track(track_id: int, db: AsyncSession = Depends(get_async_session)):
    db_track = await crud_track.delete_track(db, track_id=track_id)  # обязательно await!
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return db_track

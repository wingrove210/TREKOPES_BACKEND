from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.track import router
from routers.news import router as news_router
from routers.payment import router as payment_router
from routers.song import router as song_router
from routers.chat import router as chat_router
from core.logger import logger
from core.config import settings
from routers.assistant import router as assistant_router

app = FastAPI(
    title="Music Bot API",
    description="API для музыкального бота",
    version="1.0.0",
    docs_url="/docs",    # <-- всегда /docs
    redoc_url="/redoc"   # <-- всегда /redoc
)

# Настройка разрешенных источников
origins = [
    "*"
]

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Music Bot API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Music Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"]
)
# Монтируем статические файлы с настройками кэширования
app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads",
        html=True,
        check_dir=True,
        follow_symlink=True
    ),
    name="uploads"
)

app.include_router(router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(song_router, prefix="/api")
app.include_router(assistant_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

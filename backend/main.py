"""
StokIzleme Backend - Ana Uygulama
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import wishlist, products, notifications
from app.tasks.celery_app import celery_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış işlemleri"""
    # Veritabanı tablolarını oluştur
    Base.metadata.create_all(bind=engine)
    
    # Celery worker'ı başlat
    celery_app.conf.update(
        broker_url=settings.REDIS_URL,
        result_backend=settings.REDIS_URL,
    )
    
    yield
    
    # Temizlik işlemleri
    pass


# FastAPI uygulamasını oluştur
app = FastAPI(
    title="StokIzleme API",
    description="Wishlist stok takip uygulaması backend API'si",
    version="1.0.0",
    lifespan=lifespan
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için, production'da spesifik origin'ler belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API route'larını ekle
app.include_router(wishlist.router, prefix="/api/v1/wishlists", tags=["wishlists"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])


@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "StokIzleme API'sine Hoş Geldiniz!",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {"status": "healthy", "service": "stokizleme-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
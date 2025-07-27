"""
Uygulama konfigürasyon ayarları
"""
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, ClassVar
import os


class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # Uygulama
    APP_NAME: str = "StokIzleme"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Veritabanı
    DATABASE_URL: str = "sqlite:///./stokizleme.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Firebase (Bildirimler için)
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 gün
    
    # Web Scraping
    SCRAPING_DELAY: int = 2  # saniye
    MAX_RETRIES: int = 3
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Stok kontrolü
    STOCK_CHECK_INTERVAL: int = 30  # dakika
    NOTIFICATION_COOLDOWN: int = 60  # dakika
    
    # Mağaza ayarları
    SUPPORTED_STORES: ClassVar[Dict[str, Dict[str, str]]] = {
        "zara": {
            "base_url": "https://www.zara.com",
            "wishlist_url": "https://www.zara.com/tr/tr/wishlist",
            "product_selector": ".product-item",
            "stock_selector": ".product-availability"
        },
        "bershka": {
            "base_url": "https://www.bershka.com",
            "wishlist_url": "https://www.bershka.com/tr/wishlist",
            "product_selector": ".product-item",
            "stock_selector": ".product-availability"
        },
        "pullandbear": {
            "base_url": "https://www.pullandbear.com",
            "wishlist_url": "https://www.pullandbear.com/tr/wishlist",
            "product_selector": ".product-item",
            "stock_selector": ".product-availability"
        }
    }
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Global settings instance
settings = Settings() 
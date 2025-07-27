"""
Celery uygulama konfigürasyonu
"""
from celery import Celery
from app.core.config import settings

# Celery uygulamasını oluştur
celery_app = Celery(
    "stokizleme",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.stock_tasks"]
)

# Celery konfigürasyonu
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Istanbul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 dakika
    task_soft_time_limit=25 * 60,  # 25 dakika
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periyodik görevler
celery_app.conf.beat_schedule = {
    "check-all-wishlists": {
        "task": "app.tasks.stock_tasks.check_all_wishlists",
        "schedule": settings.STOCK_CHECK_INTERVAL * 60,  # dakikayı saniyeye çevir
    },
    "cleanup-old-notifications": {
        "task": "app.tasks.stock_tasks.cleanup_old_notifications",
        "schedule": 24 * 60 * 60,  # 24 saat
    },
} 
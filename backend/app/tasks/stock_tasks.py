"""
Stok kontrolü Celery görevleri
"""
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from loguru import logger

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.wishlist import Wishlist, WishlistItem
from app.models.notification import Notification
from app.services.scraper_service import scraper_service
from app.services.notification_service import notification_service


@celery_app.task
def check_all_wishlists():
    """Tüm aktif wishlist'leri kontrol eder"""
    logger.info("Starting stock check for all wishlists")
    
    db = SessionLocal()
    try:
        # Aktif wishlist'leri al
        active_wishlists = db.query(Wishlist).filter(Wishlist.is_active == True).all()
        
        for wishlist in active_wishlists:
            try:
                check_wishlist_stock.delay(wishlist.id)
                logger.info(f"Scheduled stock check for wishlist: {wishlist.name}")
            except Exception as e:
                logger.error(f"Error scheduling stock check for wishlist {wishlist.id}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error in check_all_wishlists: {str(e)}")
    finally:
        db.close()


@celery_app.task
def check_wishlist_stock(wishlist_id: int):
    """Belirli bir wishlist'in stok durumunu kontrol eder"""
    logger.info(f"Checking stock for wishlist ID: {wishlist_id}")
    
    db = SessionLocal()
    try:
        wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        if not wishlist:
            logger.error(f"Wishlist not found: {wishlist_id}")
            return
        
        # Wishlist'ten ürünleri çek
        products = scraper_service.scrape_wishlist(wishlist.store_name, str(wishlist.url))
        
        for product_data in products:
            try:
                # Ürünü veritabanında güncelle veya oluştur
                wishlist_item = db.query(WishlistItem).filter(
                    WishlistItem.wishlist_id == wishlist_id,
                    WishlistItem.product_id == product_data["product_id"]
                ).first()
                
                if wishlist_item:
                    # Mevcut ürünü güncelle
                    wishlist_item.product_name = product_data["product_name"]
                    wishlist_item.product_url = product_data["product_url"]
                    wishlist_item.product_image = product_data["product_image"]
                    wishlist_item.price = product_data["price"]
                    wishlist_item.size = product_data["size"]
                    wishlist_item.color = product_data["color"]
                    wishlist_item.last_checked = datetime.utcnow()
                    
                    # Stok durumu değişti mi kontrol et
                    old_stock_status = wishlist_item.is_in_stock
                    wishlist_item.is_in_stock = product_data["is_in_stock"]
                    
                    # Stok geldiyse bildirim gönder
                    if not old_stock_status and wishlist_item.is_in_stock:
                        send_stock_notification.delay(
                            wishlist_id=wishlist_id,
                            product_id=product_data["product_id"],
                            product_name=product_data["product_name"],
                            wishlist_name=wishlist.name
                        )
                        
                else:
                    # Yeni ürün ekle
                    wishlist_item = WishlistItem(
                        wishlist_id=wishlist_id,
                        product_id=product_data["product_id"],
                        product_name=product_data["product_name"],
                        product_url=product_data["product_url"],
                        product_image=product_data["product_image"],
                        price=product_data["price"],
                        size=product_data["size"],
                        color=product_data["color"],
                        is_in_stock=product_data["is_in_stock"],
                        last_checked=datetime.utcnow()
                    )
                    db.add(wishlist_item)
                
                db.commit()
                logger.info(f"Updated product: {product_data['product_name']} in wishlist: {wishlist.name}")
                
            except Exception as e:
                logger.error(f"Error processing product in wishlist {wishlist_id}: {str(e)}")
                db.rollback()
                
    except Exception as e:
        logger.error(f"Error checking wishlist stock for {wishlist_id}: {str(e)}")
    finally:
        db.close()


@celery_app.task
def send_stock_notification(wishlist_id: int, product_id: str, product_name: str, wishlist_name: str):
    """Stok bildirimi gönderir"""
    logger.info(f"Sending stock notification for product: {product_name}")
    
    db = SessionLocal()
    try:
        # Bildirim oluştur
        notification = Notification(
            wishlist_id=wishlist_id,
            product_id=product_id,
            title=f"Stok Geldi! - {wishlist_name}",
            message=f"{product_name} ürünü stokta! Hemen satın alabilirsiniz.",
            notification_type="stock_alert"
        )
        db.add(notification)
        db.commit()
        
        # Push notification gönder
        notification_service.send_push_notification(
            title=notification.title,
            message=notification.message,
            data={
                "wishlist_id": wishlist_id,
                "product_id": product_id,
                "notification_type": "stock_alert"
            }
        )
        
        # Bildirimi gönderildi olarak işaretle
        notification.is_sent = True
        notification.sent_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Stock notification sent for product: {product_name}")
        
    except Exception as e:
        logger.error(f"Error sending stock notification: {str(e)}")
        db.rollback()
    finally:
        db.close()


@celery_app.task
def cleanup_old_notifications():
    """Eski bildirimleri temizler"""
    logger.info("Cleaning up old notifications")
    
    db = SessionLocal()
    try:
        # 30 günden eski bildirimleri sil
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        deleted_count = db.query(Notification).filter(
            Notification.created_at < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(f"Deleted {deleted_count} old notifications")
        
    except Exception as e:
        logger.error(f"Error cleaning up notifications: {str(e)}")
        db.rollback()
    finally:
        db.close()


@celery_app.task
def check_single_product_stock(product_url: str, store_name: str, wishlist_item_id: int):
    """Tek bir ürünün stok durumunu kontrol eder"""
    logger.info(f"Checking stock for single product: {product_url}")
    
    db = SessionLocal()
    try:
        # Ürün stok durumunu kontrol et
        stock_info = scraper_service.check_product_stock(product_url, store_name)
        
        # Wishlist item'ı güncelle
        wishlist_item = db.query(WishlistItem).filter(WishlistItem.id == wishlist_item_id).first()
        if wishlist_item:
            old_stock_status = wishlist_item.is_in_stock
            wishlist_item.is_in_stock = stock_info["is_in_stock"]
            wishlist_item.last_checked = datetime.utcnow()
            
            # Stok geldiyse bildirim gönder
            if not old_stock_status and wishlist_item.is_in_stock:
                wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_item.wishlist_id).first()
                if wishlist:
                    send_stock_notification.delay(
                        wishlist_id=wishlist.id,
                        product_id=wishlist_item.product_id,
                        product_name=wishlist_item.product_name,
                        wishlist_name=wishlist.name
                    )
            
            db.commit()
            logger.info(f"Updated stock status for product: {wishlist_item.product_name}")
            
    except Exception as e:
        logger.error(f"Error checking single product stock: {str(e)}")
        db.rollback()
    finally:
        db.close() 
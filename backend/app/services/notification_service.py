"""
Bildirim servisi - Firebase Cloud Messaging ile push notification
"""
import json
import requests
from typing import Dict, List, Optional
from loguru import logger

from app.core.config import settings


class NotificationService:
    """Bildirim servisi"""
    
    def __init__(self):
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
        self.api_key = None  # Firebase API key buraya gelecek
        
    def send_push_notification(
        self, 
        title: str, 
        message: str, 
        data: Optional[Dict] = None,
        fcm_tokens: Optional[List[str]] = None
    ) -> bool:
        """
        Push notification gönderir
        
        Args:
            title: Bildirim başlığı
            message: Bildirim mesajı
            data: Ek veri
            fcm_tokens: FCM token listesi (None ise tüm kullanıcılara gönderir)
            
        Returns:
            Başarı durumu
        """
        try:
            if not self.api_key:
                logger.warning("Firebase API key not configured, skipping notification")
                return False
            
            # FCM payload'ı hazırla
            payload = {
                "notification": {
                    "title": title,
                    "body": message,
                    "sound": "default",
                    "badge": "1"
                },
                "data": data or {},
                "priority": "high"
            }
            
            # Token listesi varsa kullan, yoksa topic'e gönder
            if fcm_tokens:
                payload["registration_ids"] = fcm_tokens
            else:
                payload["to"] = "/topics/stokizleme"  # Tüm kullanıcılara gönder
            
            # Headers
            headers = {
                "Authorization": f"key={self.api_key}",
                "Content-Type": "application/json"
            }
            
            # FCM'e gönder
            response = requests.post(
                self.fcm_url,
                data=json.dumps(payload),
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", 0) > 0:
                    logger.info(f"Push notification sent successfully: {title}")
                    return True
                else:
                    logger.error(f"FCM error: {result}")
                    return False
            else:
                logger.error(f"FCM request failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending push notification: {str(e)}")
            return False
    
    def send_stock_alert(
        self, 
        wishlist_name: str, 
        product_name: str, 
        product_url: str,
        fcm_tokens: Optional[List[str]] = None
    ) -> bool:
        """
        Stok uyarısı gönderir
        
        Args:
            wishlist_name: Wishlist adı
            product_name: Ürün adı
            product_url: Ürün URL'i
            fcm_tokens: FCM token listesi
            
        Returns:
            Başarı durumu
        """
        title = f"Stok Geldi! - {wishlist_name}"
        message = f"{product_name} ürünü stokta! Hemen satın alabilirsiniz."
        
        data = {
            "type": "stock_alert",
            "wishlist_name": wishlist_name,
            "product_name": product_name,
            "product_url": product_url,
            "action": "open_product"
        }
        
        return self.send_push_notification(title, message, data, fcm_tokens)
    
    def send_price_drop_alert(
        self, 
        product_name: str, 
        old_price: str, 
        new_price: str,
        product_url: str,
        fcm_tokens: Optional[List[str]] = None
    ) -> bool:
        """
        Fiyat düşüşü uyarısı gönderir
        
        Args:
            product_name: Ürün adı
            old_price: Eski fiyat
            new_price: Yeni fiyat
            product_url: Ürün URL'i
            fcm_tokens: FCM token listesi
            
        Returns:
            Başarı durumu
        """
        title = f"Fiyat Düştü! - {product_name}"
        message = f"Fiyat {old_price}'den {new_price}'a düştü!"
        
        data = {
            "type": "price_drop",
            "product_name": product_name,
            "old_price": old_price,
            "new_price": new_price,
            "product_url": product_url,
            "action": "open_product"
        }
        
        return self.send_push_notification(title, message, data, fcm_tokens)
    
    def send_welcome_notification(
        self, 
        username: str,
        fcm_token: str
    ) -> bool:
        """
        Hoş geldin bildirimi gönderir
        
        Args:
            username: Kullanıcı adı
            fcm_token: FCM token
            
        Returns:
            Başarı durumu
        """
        title = "StokIzleme'e Hoş Geldiniz!"
        message = f"Merhaba {username}! Wishlist'lerinizi ekleyerek stok takibine başlayabilirsiniz."
        
        data = {
            "type": "welcome",
            "username": username,
            "action": "open_app"
        }
        
        return self.send_push_notification(title, message, data, [fcm_token])
    
    def send_test_notification(self, fcm_token: str) -> bool:
        """
        Test bildirimi gönderir
        
        Args:
            fcm_token: FCM token
            
        Returns:
            Başarı durumu
        """
        title = "Test Bildirimi"
        message = "Bu bir test bildirimidir. StokIzleme uygulaması çalışıyor!"
        
        data = {
            "type": "test",
            "action": "open_app"
        }
        
        return self.send_push_notification(title, message, data, [fcm_token])


# Global notification service instance
notification_service = NotificationService() 
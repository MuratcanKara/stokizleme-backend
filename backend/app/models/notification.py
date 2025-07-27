"""
Bildirim modeli
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Notification(Base):
    """Bildirim modeli"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    product_id = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="stock_alert")  # stock_alert, price_drop, etc.
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    wishlist = relationship("Wishlist")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title='{self.title}', sent={self.is_sent})>" 
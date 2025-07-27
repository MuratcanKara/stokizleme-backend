"""
Wishlist modelleri
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class Wishlist(Base):
    """Wishlist modeli"""
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    store_name = Column(String(50), nullable=False)  # zara, bershka, pullandbear
    url = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    auto_purchase = Column(Boolean, default=False)  # Otomatik satın alma
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # İlişkiler
    items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Wishlist(id={self.id}, name='{self.name}', store='{self.store_name}')>"


class WishlistItem(Base):
    """Wishlist ürün modeli"""
    __tablename__ = "wishlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    product_id = Column(String(100), nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    product_url = Column(Text, nullable=False)
    product_image = Column(Text)
    price = Column(String(50))
    size = Column(String(20))
    color = Column(String(50))
    is_in_stock = Column(Boolean, default=False)
    last_checked = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # İlişkiler
    wishlist = relationship("Wishlist", back_populates="items")
    
    def __repr__(self):
        return f"<WishlistItem(id={self.id}, product='{self.product_name}', in_stock={self.is_in_stock})>" 
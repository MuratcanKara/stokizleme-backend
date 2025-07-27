"""
Ürün modeli
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func

from app.core.database import Base


class Product(Base):
    """Ürün modeli"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(100), unique=True, nullable=False, index=True)
    store_name = Column(String(50), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    url = Column(Text, nullable=False)
    image_url = Column(Text)
    price = Column(Float)
    original_price = Column(Float)
    currency = Column(String(3), default="TRY")
    is_in_stock = Column(Boolean, default=False)
    available_sizes = Column(Text)  # JSON string olarak saklanacak
    available_colors = Column(Text)  # JSON string olarak saklanacak
    last_checked = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', store='{self.store_name}', in_stock={self.is_in_stock})>" 
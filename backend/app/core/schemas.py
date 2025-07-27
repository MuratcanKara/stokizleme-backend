"""
Pydantic şemaları - API request/response modelleri
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


# Wishlist Şemaları
class WishlistBase(BaseModel):
    name: str
    store_name: str
    url: HttpUrl
    auto_purchase: bool = False


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    auto_purchase: Optional[bool] = None


class WishlistItemBase(BaseModel):
    product_id: str
    product_name: str
    product_url: HttpUrl
    product_image: Optional[str] = None
    price: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None


class WishlistItemCreate(WishlistItemBase):
    pass


class WishlistItemResponse(WishlistItemBase):
    id: int
    wishlist_id: int
    is_in_stock: bool
    last_checked: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WishlistResponse(WishlistBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[WishlistItemResponse] = []

    class Config:
        from_attributes = True


# Ürün Şemaları
class ProductBase(BaseModel):
    product_id: str
    store_name: str
    name: str
    url: HttpUrl
    image_url: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    currency: str = "TRY"


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    is_in_stock: bool
    available_sizes: Optional[str] = None
    available_colors: Optional[str] = None
    last_checked: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Bildirim Şemaları
class NotificationBase(BaseModel):
    wishlist_id: int
    product_id: str
    title: str
    message: str
    notification_type: str = "stock_alert"


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Kullanıcı Şemaları
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    fcm_token: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# API Response Şemaları
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int 
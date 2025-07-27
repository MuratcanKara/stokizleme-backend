"""
Wishlist API route'ları
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.schemas import (
    WishlistCreate, 
    WishlistUpdate, 
    WishlistResponse,
    WishlistItemCreate,
    WishlistItemResponse,
    APIResponse
)
from app.models.wishlist import Wishlist, WishlistItem
from app.services.scraper_service import scraper_service
from app.tasks.stock_tasks import check_wishlist_stock

router = APIRouter()


@router.post("/", response_model=WishlistResponse)
async def create_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db)
):
    """Yeni wishlist oluşturur"""
    try:
        # Wishlist oluştur
        db_wishlist = Wishlist(
            name=wishlist.name,
            store_name=wishlist.store_name,
            url=str(wishlist.url),
            auto_purchase=wishlist.auto_purchase
        )
        db.add(db_wishlist)
        db.commit()
        db.refresh(db_wishlist)
        
        # Wishlist'ten ürünleri çek
        products = await scraper_service.scrape_wishlist(
            wishlist.store_name, 
            str(wishlist.url)
        )
        
        # Ürünleri veritabanına ekle
        for product_data in products:
            wishlist_item = WishlistItem(
                wishlist_id=db_wishlist.id,
                product_id=product_data["product_id"],
                product_name=product_data["product_name"],
                product_url=product_data["product_url"],
                product_image=product_data["product_image"],
                price=product_data["price"],
                size=product_data["size"],
                color=product_data["color"],
                is_in_stock=product_data["is_in_stock"]
            )
            db.add(wishlist_item)
        
        db.commit()
        db.refresh(db_wishlist)
        
        return db_wishlist
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating wishlist: {str(e)}"
        )


@router.get("/", response_model=List[WishlistResponse])
async def get_wishlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Tüm wishlist'leri getirir"""
    wishlists = db.query(Wishlist).offset(skip).limit(limit).all()
    return wishlists


@router.get("/{wishlist_id}", response_model=WishlistResponse)
async def get_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    """Belirli bir wishlist'i getirir"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    return wishlist


@router.put("/{wishlist_id}", response_model=WishlistResponse)
async def update_wishlist(
    wishlist_id: int,
    wishlist_update: WishlistUpdate,
    db: Session = Depends(get_db)
):
    """Wishlist'i günceller"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    
    # Güncelleme verilerini uygula
    update_data = wishlist_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(wishlist, field, value)
    
    db.commit()
    db.refresh(wishlist)
    return wishlist


@router.delete("/{wishlist_id}", response_model=APIResponse)
async def delete_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    """Wishlist'i siler"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    
    db.delete(wishlist)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Wishlist deleted successfully"
    )


@router.post("/{wishlist_id}/refresh", response_model=APIResponse)
async def refresh_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    """Wishlist'i yeniler (ürünleri tekrar çeker)"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    
    # Celery task'ı başlat
    check_wishlist_stock.delay(wishlist_id)
    
    return APIResponse(
        success=True,
        message="Wishlist refresh started"
    )


@router.post("/{wishlist_id}/toggle-auto-purchase", response_model=WishlistResponse)
async def toggle_auto_purchase(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    """Otomatik satın alma özelliğini açıp kapatır"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    
    wishlist.auto_purchase = not wishlist.auto_purchase
    db.commit()
    db.refresh(wishlist)
    
    return wishlist


@router.get("/{wishlist_id}/items", response_model=List[WishlistItemResponse])
async def get_wishlist_items(
    wishlist_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Wishlist'teki ürünleri getirir"""
    items = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id
    ).offset(skip).limit(limit).all()
    return items


@router.post("/{wishlist_id}/items", response_model=WishlistItemResponse)
async def add_wishlist_item(
    wishlist_id: int,
    item: WishlistItemCreate,
    db: Session = Depends(get_db)
):
    """Wishlist'e yeni ürün ekler"""
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    
    wishlist_item = WishlistItem(
        wishlist_id=wishlist_id,
        product_id=item.product_id,
        product_name=item.product_name,
        product_url=str(item.product_url),
        product_image=item.product_image,
        price=item.price,
        size=item.size,
        color=item.color
    )
    
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    
    return wishlist_item


@router.delete("/{wishlist_id}/items/{item_id}", response_model=APIResponse)
async def remove_wishlist_item(
    wishlist_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Wishlist'ten ürün çıkarır"""
    item = db.query(WishlistItem).filter(
        WishlistItem.id == item_id,
        WishlistItem.wishlist_id == wishlist_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Item removed from wishlist"
    ) 
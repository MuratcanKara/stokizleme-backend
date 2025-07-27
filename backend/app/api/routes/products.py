"""
Products API route'ları
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.schemas import ProductResponse, APIResponse
from app.models.product import Product
from app.services.scraper_service import scraper_service
from app.tasks.stock_tasks import check_single_product_stock

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    store_name: str = None,
    in_stock: bool = None,
    db: Session = Depends(get_db)
):
    """Tüm ürünleri getirir"""
    query = db.query(Product)
    
    if store_name:
        query = query.filter(Product.store_name == store_name)
    
    if in_stock is not None:
        query = query.filter(Product.is_in_stock == in_stock)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Belirli bir ürünü getirir"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/check-stock", response_model=APIResponse)
async def check_product_stock(
    product_url: str,
    store_name: str,
    db: Session = Depends(get_db)
):
    """Ürün stok durumunu kontrol eder"""
    try:
        stock_info = await scraper_service.check_product_stock(product_url, store_name)
        
        return APIResponse(
            success=True,
            message="Stock check completed",
            data=stock_info
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking stock: {str(e)}"
        )


@router.get("/in-stock", response_model=List[ProductResponse])
async def get_in_stock_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Stokta olan ürünleri getirir"""
    products = db.query(Product).filter(
        Product.is_in_stock == True
    ).offset(skip).limit(limit).all()
    return products


@router.get("/out-of-stock", response_model=List[ProductResponse])
async def get_out_of_stock_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Stokta olmayan ürünleri getirir"""
    products = db.query(Product).filter(
        Product.is_in_stock == False
    ).offset(skip).limit(limit).all()
    return products 
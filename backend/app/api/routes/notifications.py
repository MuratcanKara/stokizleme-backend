"""
Notifications API route'ları
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.schemas import NotificationResponse, APIResponse
from app.models.notification import Notification
from app.services.notification_service import notification_service

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    is_sent: bool = None,
    notification_type: str = None,
    db: Session = Depends(get_db)
):
    """Tüm bildirimleri getirir"""
    query = db.query(Notification)
    
    if is_sent is not None:
        query = query.filter(Notification.is_sent == is_sent)
    
    if notification_type:
        query = query.filter(Notification.notification_type == notification_type)
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Belirli bir bildirimi getirir"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification


@router.post("/test", response_model=APIResponse)
async def send_test_notification(
    fcm_token: str,
    db: Session = Depends(get_db)
):
    """Test bildirimi gönderir"""
    try:
        success = notification_service.send_test_notification(fcm_token)
        
        if success:
            return APIResponse(
                success=True,
                message="Test notification sent successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send test notification"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending test notification: {str(e)}"
        )


@router.delete("/{notification_id}", response_model=APIResponse)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Bildirimi siler"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Notification deleted successfully"
    )


@router.delete("/", response_model=APIResponse)
async def clear_all_notifications(
    db: Session = Depends(get_db)
):
    """Tüm bildirimleri temizler"""
    try:
        deleted_count = db.query(Notification).delete()
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"Deleted {deleted_count} notifications"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing notifications: {str(e)}"
        ) 
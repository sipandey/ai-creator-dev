from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime  # CHANGE: Added missing datetime import
import os  
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.persona_schema import VideoProcessingRequest
from app.services.multi_modal_persona_service import MultiModalPersonaService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persona/enhanced", tags=["Enhanced Persona"])

@router.post("/create-from-videos", response_model=Dict[str, Any])
async def create_persona_from_videos(
    request: VideoProcessingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create enhanced persona from video URLs with comprehensive processing"""
    try:
        # Assign creator_id from the authenticated user
        request.creator_id = current_user.id
        
        if not request.video_urls:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one video URL is required"
            )
        
        if len(request.video_urls) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 5 video URLs allowed"
            )
        
        logger.info(f"Creating persona for user {request.creator_id} with {len(request.video_urls)} videos")
        
        # Process videos and create persona
        service = MultiModalPersonaService(db)
        result = await service.create_persona_from_videos(request)
        
        # Log success metrics
        processing_summary = result.get('processing_summary', {})
        logger.info(f"Persona creation completed - Success rate: {processing_summary.get('successful_extractions', 0)}/{len(request.video_urls)}")
        
        return {
            "success": True,
            "message": "Enhanced persona created successfully from video content",
            "data": result
        }
        
    except ValueError as e:
        logger.warning(f"Validation error for user {request.creator_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating persona for user {request.creator_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing videos"
        )

@router.get("/status/{creator_id}", response_model=Dict[str, Any])
async def get_persona_status(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get persona processing status and quality metrics"""
    try:
        if creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view your own persona status"
            )
        
        service = MultiModalPersonaService(db)
        persona_data = service.get_persona_by_creator(creator_id)
        
        if not persona_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona not found"
            )
        
        # Extract status information
        status_info = {
            "persona_exists": True,
            "confidence_score": persona_data.get('confidence_score', 0),
            "last_updated": persona_data.get('last_updated'),
            "version": persona_data.get('version', 'v1'),
            "content_sources": persona_data.get('content_sources', []),
            "processing_metadata": persona_data.get('processing_metadata', {}),
            "quality_metrics": {
                "data_richness": len(persona_data.get('content_sources', [])),
                "confidence_level": "high" if persona_data.get('confidence_score', 0) > 0.7 else "medium" if persona_data.get('confidence_score', 0) > 0.4 else "low",
                "completeness": "complete" if persona_data.get('confidence_score', 0) > 0.6 else "partial"
            }
        }
        
        return {
            "success": True,
            "data": status_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting persona status for creator {creator_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving persona status"
        )

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint for enhanced persona service"""
    try:
        # Check service dependencies
        health_status = {
            "service": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "dependencies": {
                "rapidapi_configured": bool(os.getenv('RAPIDAPI_KEY')),
                "openai_configured": bool(os.getenv('OPENAI_API_KEY')),
                "google_speech_configured": bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')),
                "azure_speech_configured": bool(os.getenv('AZURE_SPEECH_KEY'))
            }
        }
        
        return {
            "success": True,
            "data": health_status
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )

@router.get("/", response_model=Dict[str, Any])
async def get_my_persona(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the current user's persona"""
    try:
        service = MultiModalPersonaService(db)
        persona_data = service.get_persona_by_creator(current_user.id)
        
        if not persona_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona not found for the current user."
            )
        
        return {
            "success": True,
            "data": persona_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting persona for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving persona."
        )

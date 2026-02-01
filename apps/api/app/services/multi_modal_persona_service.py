from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.persona import CreatorPersona
from app.models.user import User
from app.services.video_processing_service import VideoProcessingService
from app.agents.enhanced_style_analysis_agent import EnhancedStyleAnalysisAgent
from app.schemas.persona_schema import PersonaV2, VideoProcessingRequest
from app.services.strategy_service import StrategyService
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class MultiModalPersonaService:
    """Production-grade multi-modal persona service with LLM-driven analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        # Lazy load heavy services to avoid overhead on lightweight requests
        self._video_processor = None
        self._style_analyzer = None
        self._strategy_service = None

    @property
    def video_processor(self):
        if not self._video_processor:
            self._video_processor = VideoProcessingService()
        return self._video_processor

    @property
    def style_analyzer(self):
        if not self._style_analyzer:
            self._style_analyzer = EnhancedStyleAnalysisAgent()
        return self._style_analyzer

    @property
    def strategy_service(self):
        if not self._strategy_service:
            self._strategy_service = StrategyService(self.db)
        return self._strategy_service
    
    async def create_persona_from_videos(self, request: VideoProcessingRequest) -> Dict[str, Any]:
        """Create persona from video URLs with comprehensive error handling"""
        try:
            # Validate user
            user = self.db.query(User).filter(User.id == request.creator_id).first()
            if not user:
                raise ValueError(f"User {request.creator_id} not found")
            
            logger.info(f"Creating persona for user {request.creator_id} with {len(request.video_urls)} videos")
            
            # Process video URLs
            video_results = await self.video_processor.process_video_urls(request.video_urls)
            
            # Prepare content for analysis
            extracted_content = video_results.get('extracted_content', [])
            processing_metadata = video_results.get('processing_metadata', [])
            errors = video_results.get('errors', [])
            
            # Combine with text samples
            all_text_samples = request.sample_texts or []
            
            # Ensure we have content to analyze
            if not extracted_content and not all_text_samples:
                if errors:
                    error_details = "; ".join([f"{e['url']}: {e['error']}" for e in errors])
                    raise ValueError(f"No content extracted from videos. Errors: {error_details}")
                else:
                    raise ValueError("No content available for analysis")
            
            # Generate persona using LLM analysis
            persona_data = await self.style_analyzer.analyze_multi_modal_content(
                text_samples=all_text_samples,
                video_content=extracted_content,
                processing_metadata=processing_metadata
            )
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(
                text_samples=all_text_samples,
                video_content=extracted_content,
                errors=errors
            )
            persona_data['confidence_score'] = confidence
            
            # Add metadata
            persona_data['content_sources'] = self._build_content_sources(
                all_text_samples, extracted_content
            )
            persona_data['last_updated'] = datetime.utcnow().isoformat()
            persona_data['processing_version'] = '2.0'
            
            # Save to database
            persona = await self._save_persona(request.creator_id, persona_data)

            # Regenerate weekly strategy based on new persona
            try:
                logger.info(f"Regenerating strategy for user {request.creator_id} after persona update")
                self.strategy_service.regenerate_weekly_strategy(request.creator_id)
            except Exception as e:
                logger.error(f"Failed to regenerate strategy for user {request.creator_id}: {str(e)}")
                # Don't fail persona creation if strategy regeneration fails
                pass
            
            return {
                'persona': persona_data,
                'processing_summary': {
                    'videos_processed': len(request.video_urls),
                    'successful_extractions': len(extracted_content),
                    'text_samples_used': len(all_text_samples),
                    'confidence_score': confidence,
                    'errors': errors,
                    'processing_method': 'llm_multi_modal'
                }
            }
            
        except ValueError as e:
            logger.error(f"Validation error creating persona: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating persona: {str(e)}")
            raise ValueError(f"Failed to create persona: {str(e)}")
    
    def _calculate_confidence_score(
        self, 
        text_samples: List[str], 
        video_content: List[Dict[str, Any]], 
        errors: List[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score based on available content and processing success"""
        base_score = 0.2
        
        # Points for text samples
        text_points = min(len(text_samples) * 0.1, 0.3)
        
        # Points for video content (higher weight)
        video_points = min(len(video_content) * 0.2, 0.5)
        
        # Penalty for errors
        error_penalty = min(len(errors) * 0.1, 0.3)
        
        # Bonus for high-quality extractions
        quality_bonus = 0.0
        for content in video_content:
            metadata = content.get('metadata', {})
            if metadata.get('confidence_score', 0) > 0.7:
                quality_bonus += 0.05
        
        total_score = base_score + text_points + video_points + quality_bonus - error_penalty
        return min(max(total_score, 0.1), 0.95)
    
    def _build_content_sources(
        self, 
        text_samples: List[str], 
        video_content: List[Dict[str, Any]]
    ) -> List[str]:
        """Build content sources tracking"""
        sources = []
        
        if text_samples:
            sources.extend([f"text_sample_{i}" for i in range(len(text_samples))])
        
        for i, content in enumerate(video_content):
            metadata = content.get('metadata', {})
            processing_method = metadata.get('processing_method', 'unknown')
            sources.append(f"video_{i}_{processing_method}")
        
        return sources
    
    async def _save_persona(self, creator_id: int, persona_data: Dict[str, Any]) -> CreatorPersona:
        """Save persona with enhanced error handling"""
        try:
            existing = self.db.query(CreatorPersona).filter(
                CreatorPersona.user_id == creator_id  # CHANGE: Fixed attribute name from creator_id to user_id
            ).first()
            
            if existing:
                # Update existing
                existing.persona_json = json.dumps(persona_data)  # CHANGE: Fixed attribute name from persona_json to persona_data
                existing.confidence_score = persona_data.get('confidence_score', 0.5)
                existing.version = 'v2'
                existing.updated_at = datetime.utcnow()
                logger.info(f"Updated existing persona for creator {creator_id}")
            else:
                # Create new
                existing = CreatorPersona(
                    user_id=creator_id,
                    persona_json=json.dumps(persona_data),
                    confidence_score=persona_data.get('confidence_score', 0.5),
                    version='v2',
                    source='multi_modal_llm'
                )
                self.db.add(existing)
                logger.info(f"Created new persona for creator {creator_id}")
            
            self.db.commit()
            self.db.refresh(existing)
            return existing
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving persona for creator {creator_id}: {str(e)}")
            raise
    
    def get_persona_by_creator(self, creator_id: int) -> Optional[Dict[str, Any]]:
        """Get persona with error handling"""
        try:
            persona = self.db.query(CreatorPersona).filter(
                CreatorPersona.user_id == creator_id
            ).first()
            
            if persona:
                return json.loads(persona.persona_json)
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving persona for creator {creator_id}: {str(e)}")
            return None
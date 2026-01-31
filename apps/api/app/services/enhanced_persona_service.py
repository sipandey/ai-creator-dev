from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.persona import CreatorPersona
from app.models.enhanced_models import ContentSource, PersonaVersion
from app.models.user import User
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class EnhancedPersonaService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_persona_with_sources(
        self,
        creator_id: int,
        persona_data: Dict[str, Any],
        content_sources: List[Dict[str, Any]]
    ) -> CreatorPersona:
        """Create persona with content source tracking"""
        try:
            # Check if persona already exists
            existing_persona = self.db.query(CreatorPersona).filter(
                CreatorPersona.user_id == creator_id
            ).first()
            
            if existing_persona:
                # Update existing persona
                return self._update_existing_persona(existing_persona, persona_data, content_sources)
            else:
                # Create new persona
                return self._create_new_persona(creator_id, persona_data, content_sources)
                
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating persona with sources: {str(e)}")
            raise
    
    def _create_new_persona(
        self,
        creator_id: int,
        persona_data: Dict[str, Any],
        content_sources: List[Dict[str, Any]]
    ) -> CreatorPersona:
        """Create new persona entry"""
        # Create content source records
        source_ids = []
        for source_data in content_sources:
            content_source = ContentSource(
                creator_id=creator_id,
                source_url=source_data.get('url'),
                source_type=source_data.get('type', 'manual'),
                platform=source_data.get('platform'),
                content_data=source_data.get('data'),
                confidence_contribution=source_data.get('confidence', 0.0)
            )
            self.db.add(content_source)
            self.db.flush()  # Get ID without committing
            source_ids.append(content_source.id)
        
        # Create persona with source tracking
        persona = CreatorPersona(
            user_id=creator_id,
            persona_json=persona_data,
            confidence_score=persona_data.get('confidence_score', 0.5),
            source='enhanced_analysis',
            version='v2',
            content_sources=source_ids,
            processing_metadata={
                'created_at': datetime.utcnow().isoformat(),
                'source_count': len(content_sources),
                'processing_version': '2.0'
            }
        )
        self.db.add(persona)
        
        # Create version record
        self._create_persona_version(creator_id, 1, persona_data, "Initial persona creation")
        
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def _update_existing_persona(
        self,
        existing_persona: CreatorPersona,
        new_persona_data: Dict[str, Any],
        content_sources: List[Dict[str, Any]]
    ) -> CreatorPersona:
        """Update existing persona with new data"""
        # Get current version number
        latest_version = self.db.query(PersonaVersion).filter(
            PersonaVersion.creator_id == existing_persona.user_id
        ).order_by(PersonaVersion.version_number.desc()).first()
        
        next_version = (latest_version.version_number + 1) if latest_version else 1
        
        # Add new content sources
        new_source_ids = []
        for source_data in content_sources:
            content_source = ContentSource(
                creator_id=existing_persona.user_id,
                source_url=source_data.get('url'),
                source_type=source_data.get('type', 'manual'),
                platform=source_data.get('platform'),
                content_data=source_data.get('data'),
                confidence_contribution=source_data.get('confidence', 0.0)
            )
            self.db.add(content_source)
            self.db.flush()
            new_source_ids.append(content_source.id)
        
        # Merge with existing sources
        existing_sources = existing_persona.content_sources or []
        all_sources = existing_sources + new_source_ids
        
        # Update persona
        existing_persona.persona_json = new_persona_data
        existing_persona.confidence_score = new_persona_data.get('confidence_score', existing_persona.confidence_score)
        existing_persona.version = 'v2'
        existing_persona.content_sources = all_sources
        existing_persona.updated_at = datetime.utcnow()
        
        # Update processing metadata
        existing_metadata = existing_persona.processing_metadata or {}
        existing_metadata.update({
            'last_updated': datetime.utcnow().isoformat(),
            'total_sources': len(all_sources),
            'latest_update_sources': len(new_source_ids)
        })
        existing_persona.processing_metadata = existing_metadata
        
        # Create version record
        change_summary = f"Updated with {len(content_sources)} new sources"
        self._create_persona_version(existing_persona.user_id, next_version, new_persona_data, change_summary)
        
        self.db.commit()
        self.db.refresh(existing_persona)
        return existing_persona
    
    def _create_persona_version(
        self,
        creator_id: int,
        version_number: int,
        persona_data: Dict[str, Any],
        change_summary: str
    ):
        """Create persona version record"""
        version_record = PersonaVersion(
            creator_id=creator_id,
            version_number=version_number,
            persona_data=persona_data,
            confidence_score=persona_data.get('confidence_score'),
            change_summary=change_summary
        )
        self.db.add(version_record)
    
    def get_persona_with_sources(self, creator_id: int) -> Optional[Dict[str, Any]]:
        """Get persona with content source information"""
        persona = self.db.query(CreatorPersona).filter(
            CreatorPersona.user_id == creator_id
        ).first()
        
        if not persona:
            return None
        
        # Get content sources
        source_ids = persona.content_sources or []
        content_sources = self.db.query(ContentSource).filter(
            ContentSource.id.in_(source_ids),
            ContentSource.is_active == True
        ).all()
        
        return {
            'persona_data': persona.persona_json,
            'confidence_score': persona.confidence_score,
            'version': persona.version,
            'content_sources': [
                {
                    'id': source.id,
                    'type': source.source_type,
                    'platform': source.platform,
                    'url': source.source_url,
                    'processed_at': source.processed_at.isoformat() if source.processed_at else None,
                    'confidence_contribution': source.confidence_contribution
                }
                for source in content_sources
            ],
            'processing_metadata': persona.processing_metadata,
            'updated_at': persona.updated_at.isoformat() if persona.updated_at else None
        }
    
    def get_persona_history(self, creator_id: int) -> List[Dict[str, Any]]:
        """Get persona version history"""
        versions = self.db.query(PersonaVersion).filter(
            PersonaVersion.creator_id == creator_id
        ).order_by(PersonaVersion.version_number.desc()).all()
        
        return [
            {
                'version_number': version.version_number,
                'confidence_score': version.confidence_score,
                'change_summary': version.change_summary,
                'created_at': version.created_at.isoformat() if version.created_at else None
            }
            for version in versions
        ]
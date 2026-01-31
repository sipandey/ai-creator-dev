import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.llm.client import call_llm
from app.schemas.persona_schema import PersonaV2

logger = logging.getLogger(__name__)

class EnhancedStyleAnalysisAgent:
    """Production-grade style analysis agent with LLM-driven insights"""
    
    def __init__(self):
        self.system_prompt = """
You are an expert content strategist and human behavior analyst specializing in creator persona extraction.

Your expertise:
- Deep understanding of human communication patterns and authenticity markers
- Analysis of multi-modal content (text, video, audio) for personality insights
- Extraction of subtle characteristics that make content feel genuinely human
- Recognition of cultural nuances and platform-specific communication styles

Your task:
Analyze creator content from multiple sources to extract a comprehensive, human-like persona that captures their unique characteristics and communication style.

Critical requirements:
- Output ONLY valid JSON matching the PersonaV2 schema
- Focus on authentic human traits, not generic content patterns
- Identify subtle communication nuances that distinguish this creator
- Extract emotional intelligence and empathy markers
- Recognize consistency patterns across different content types
- Assign confidence scores based on data quality and behavioral consistency
"""

    async def analyze_multi_modal_content(
        self, 
        text_samples: List[str], 
        video_content: List[Dict[str, Any]],
        processing_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze multi-modal content using advanced LLM reasoning"""
        
        try:
            # Prepare comprehensive content summary
            content_analysis = self._prepare_content_for_llm_analysis(
                text_samples, video_content, processing_metadata
            )
            
            # Generate persona using advanced prompting
            persona_data = await self._generate_persona_with_llm(content_analysis)
            
            # Validate and enhance persona
            validated_persona = self._validate_and_enhance_persona(persona_data)
            
            return validated_persona
            
        except Exception as e:
            logger.error(f"Multi-modal analysis failed: {str(e)}")
            return self._get_fallback_persona()
    
    def _prepare_content_for_llm_analysis(
        self,
        text_samples: List[str],
        video_content: List[Dict[str, Any]], 
        processing_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Prepare content for comprehensive LLM analysis"""
        
        # Extract video insights
        video_insights = []
        detected_languages = []
        for content in video_content:
            content_data = content.get('content', {})
            language = content_data.get('language', 'english')
            detected_languages.append(language)
            video_insights.append({
                'transcript': content_data.get('transcript', ''),
                'topics': content_data.get('main_topics', []),
                'language': language,  # Add detected language
                'style_markers': content_data.get('style_markers', {}),
                'visual_characteristics': content_data.get('visual_characteristics', {}),
                'confidence': content.get('metadata', {}).get('confidence_score', 0.5)
            })
        
        # Log detected languages for debugging
        if detected_languages:
            logger.info(f"Detected languages from video content: {detected_languages}")
            # Determine primary language (use most common)
            primary_language = max(set(detected_languages), key=detected_languages.count)
            logger.info(f"Primary language determined: {primary_language}")
        else:
            primary_language = 'english'
            logger.info("No language detected from video content, defaulting to english")
        
        # Aggregate processing metadata
        processing_summary = {
            'total_sources': len(text_samples) + len(video_content),
            'extraction_methods': list(set([
                meta.get('processing_method', 'unknown') 
                for meta in processing_metadata
            ])),
            'average_confidence': sum([
                meta.get('confidence_score', 0.5) 
                for meta in processing_metadata
            ]) / max(len(processing_metadata), 1)
        }
        
        return {
            'text_samples': text_samples[:5],  # Limit for token efficiency
            'video_insights': video_insights[:5],
            'processing_summary': processing_summary,
            'detected_primary_language': primary_language,  # Add primary language
            'analysis_timestamp': datetime.utcnow().isoformat()
        }
    
    async def _generate_persona_with_llm(self, content_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate persona using advanced LLM analysis"""
        
        user_prompt = f"""
Analyze this comprehensive creator content to extract an authentic, human-like persona:

CONTENT ANALYSIS:
{json.dumps(content_analysis, indent=2)}

IMPORTANT: The primary language detected from audio analysis is: {content_analysis.get('detected_primary_language', 'english')}

Extract a detailed persona using this exact JSON schema:

{{
  "language": "{content_analysis.get('detected_primary_language', 'english')}",
  "tone": ["empathetic", "honest", "informative", "motivational", "humorous", "professional", "casual"],
  "energy_level": "low | medium | high",
  "hook_style": "problem-first | story-first | fact-first",
  "cta_style": "soft | direct | follow",
  "formats": ["talking-head", "text-overlay", "b-roll", "tutorial", "lifestyle"],
  "topics": ["specific topics based on content"],
  "pacing": "slow | moderate | fast",
  "communication_patterns": {{
    "sentence_complexity": "simple | moderate | complex",
    "vocabulary_level": "casual | professional | academic",
    "filler_words": ["specific filler words used"],
    "signature_phrases": ["unique phrases this creator uses"],
    "question_frequency": "low | medium | high"
  }},
  "emotional_markers": {{
    "enthusiasm_indicators": ["specific enthusiasm markers"],
    "vulnerability_expressions": ["ways they show vulnerability"],
    "humor_style": "witty | sarcastic | wholesome | dry | none",
    "empathy_level": "low | medium | high",
    "authenticity_markers": ["specific authenticity indicators"]
  }},
  "visual_preferences": {{
    "color_schemes": ["preferred colors from content"],
    "text_positioning": "top | center | bottom | dynamic",
    "visual_metaphors": ["visual elements they use"],
    "background_style": "minimal | busy | branded | natural"
  }},
  "timing_patterns": {{
    "pause_frequency": "low | medium | high",
    "speech_rhythm": "steady | varied | dramatic",
    "content_pacing": "slow | moderate | fast",
    "hook_timing": 3.5
  }},
  "confidence_score": 0.85,
  "content_sources": ["text", "video"],
  "version": "v2"
}}

Analysis Guidelines:
1. Extract SPECIFIC characteristics unique to this creator
2. Focus on authentic human traits that make content feel personal
3. Identify subtle communication patterns and emotional intelligence
4. Consider cultural context and platform-specific adaptations
5. Weight video insights more heavily as they contain richer behavioral data
6. Ensure consistency across different content types
7. Assign confidence based on data quality and behavioral consistency

Provide specific, actionable insights that would help generate content that feels authentically like this creator.
"""

        try:
            llm_response = call_llm(self.system_prompt, user_prompt)
            
            # Clean and parse response
            cleaned_response = self._clean_llm_response(llm_response)
            persona_data = json.loads(cleaned_response)
            
            logger.info("LLM persona generation successful")
            return persona_data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"LLM returned invalid JSON: {str(e)}")
            raise ValueError(f"LLM persona generation failed: {str(e)}")
    
    def _clean_llm_response(self, response: str) -> str:
        """Clean and extract JSON from LLM response"""
        if not response:
            raise ValueError("Empty LLM response")
        
        response = response.strip()
        
        # Extract JSON content
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            raise ValueError("No valid JSON found in LLM response")
        
        return response[start_idx:end_idx + 1]
    
    def _validate_and_enhance_persona(self, persona_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate persona against schema and enhance with additional insights"""
        try:
            # Validate against PersonaV2 schema
            persona = PersonaV2(**persona_data)
            validated_data = persona.dict()
            
            # Add processing metadata
            validated_data['processing_metadata'] = {
                'analysis_method': 'llm_multi_modal',
                'validation_passed': True,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return validated_data
            
        except Exception as e:
            logger.error(f"Persona validation failed: {str(e)}")
            # Return enhanced fallback
            return self._get_enhanced_fallback_persona(persona_data)
    
    def _get_enhanced_fallback_persona(self, partial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced fallback persona using partial LLM data"""
        fallback = self._get_fallback_persona()
        
        # Merge any valid data from LLM response
        for key, value in partial_data.items():
            if key in fallback and value:
                try:
                    fallback[key] = value
                except Exception:
                    continue
        
        fallback['processing_metadata'] = {
            'analysis_method': 'llm_fallback',
            'validation_passed': False,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return fallback
    
    def _get_fallback_persona(self) -> Dict[str, Any]:
        """Comprehensive fallback persona for error cases"""
        return {
            "language": "english",
            "tone": ["informative", "friendly", "authentic"],
            "energy_level": "medium",
            "hook_style": "problem-first",
            "cta_style": "soft",
            "formats": ["talking-head", "educational"],
            "topics": ["general", "lifestyle"],
            "pacing": "moderate",
            "communication_patterns": {
                "sentence_complexity": "moderate",
                "vocabulary_level": "casual",
                "filler_words": ["um", "like"],
                "signature_phrases": ["hey everyone", "let me share"],
                "question_frequency": "medium"
            },
            "emotional_markers": {
                "enthusiasm_indicators": ["exclamation marks", "energy words"],
                "vulnerability_expressions": ["personal stories"],
                "humor_style": "wholesome",
                "empathy_level": "medium",
                "authenticity_markers": ["personal anecdotes", "behind-the-scenes"]
            },
            "visual_preferences": {
                "color_schemes": ["#FF6B6B", "#4ECDC4"],
                "text_positioning": "center",
                "visual_metaphors": ["everyday objects"],
                "background_style": "minimal"
            },
            "timing_patterns": {
                "pause_frequency": "medium",
                "speech_rhythm": "steady",
                "content_pacing": "moderate",
                "hook_timing": 3.0
            },
            "confidence_score": 0.3,
            "content_sources": ["fallback"],
            "version": "v2"
        }
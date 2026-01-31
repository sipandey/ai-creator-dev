from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Language(str, Enum):
    ENGLISH = "english"
    HINGLISH = "hinglish"
    HINDI = "hindi"

class EnergyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class HookStyle(str, Enum):
    PROBLEM_FIRST = "problem-first"
    STORY_FIRST = "story-first"
    FACT_FIRST = "fact-first"

class CTAStyle(str, Enum):
    SOFT = "soft"
    DIRECT = "direct"
    FOLLOW = "follow"

class Pacing(str, Enum):
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"

class HumorStyle(str, Enum):
    WITTY = "witty"
    SARCASTIC = "sarcastic"
    WHOLESOME = "wholesome"
    DRY = "dry"
    NONE = "none"

class VulnerabilityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class CommunicationPattern(BaseModel):
    sentence_complexity: str = Field(..., description="simple | moderate | complex")
    vocabulary_level: str = Field(..., description="casual | professional | academic")
    filler_words: List[str] = Field(default_factory=list)
    signature_phrases: List[str] = Field(default_factory=list)
    question_frequency: str = Field(..., description="low | medium | high")

class EmotionalMarkers(BaseModel):
    enthusiasm_indicators: List[str] = Field(default_factory=list)
    vulnerability_expressions: List[str] = Field(default_factory=list)
    humor_style: HumorStyle
    empathy_level: str = Field(..., description="low | medium | high")
    authenticity_markers: List[str] = Field(default_factory=list)

class VisualPreferences(BaseModel):
    color_schemes: List[str] = Field(default_factory=list)
    text_positioning: str = Field(..., description="top | center | bottom | dynamic")
    visual_metaphors: List[str] = Field(default_factory=list)
    background_style: str = Field(..., description="minimal | busy | branded | natural")

class TimingPatterns(BaseModel):
    pause_frequency: str = Field(..., description="low | medium | high")
    speech_rhythm: str = Field(..., description="steady | varied | dramatic")
    content_pacing: Pacing
    hook_timing: float = Field(..., description="Seconds to hook in video")

class PersonaV2(BaseModel):
    # Core attributes (v1)
    language: Language
    tone: List[str]
    energy_level: EnergyLevel
    hook_style: HookStyle
    cta_style: CTAStyle
    formats: List[str]
    topics: List[str]
    pacing: Pacing
    
    # Enhanced attributes (v2)
    communication_patterns: CommunicationPattern
    emotional_markers: EmotionalMarkers
    visual_preferences: VisualPreferences
    timing_patterns: TimingPatterns
    
    # Metadata
    confidence_score: float = Field(ge=0.0, le=1.0)
    content_sources: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None
    version: str = "v2"

class VideoProcessingRequest(BaseModel):
    video_urls: List[str] = Field(..., max_items=5)
    sample_texts: Optional[List[str]] = Field(default_factory=list)
    creator_id: Optional[int] = None

class ContentSource(BaseModel):
    url: str
    platform: str
    content_type: str = Field(..., description="video | text")
    processed_at: str
    confidence: float

class CreatorPersonaResponse(BaseModel):
    id: int
    user_id: int
    persona_json: Dict[str, Any]
    confidence_score: Optional[float]
    source: str
    version: Optional[str]
    content_sources: Optional[List[str]] = None
    processing_metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

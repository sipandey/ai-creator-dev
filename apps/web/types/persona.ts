export interface Persona {
  language: string;
  tone: string[];
  energy_level: "low" | "medium" | "high";
  hook_style: "problem-first" | "story-first" | "fact-first";
  cta_style: "soft" | "direct" | "follow";
  formats: string[];
  topics: string[];
  pacing: "slow" | "moderate" | "fast";
  communication_patterns: {
    sentence_complexity: string;
    vocabulary_level: string;
    filler_words: string[];
    signature_phrases: string[];
    question_frequency: string;
  };
  emotional_markers: {
    enthusiasm_indicators: string[];
    vulnerability_expressions: string[];
    humor_style: string;
    empathy_level: string;
    authenticity_markers: string[];
  };
  visual_preferences: {
    color_schemes: string[];
    text_positioning: string;
    visual_metaphors: string[];
    background_style: string;
  };
  timing_patterns: {
    pause_frequency: string;
    speech_rhythm: string;
    content_pacing: string;
    hook_timing: number;
  };
  confidence_score: number;
  content_sources: string[];
  last_updated: string;
  version: string;
  processing_metadata?: {
    analysis_method: string;
    validation_passed: boolean;
    generated_at: string;
  };
  processing_version?: string;
}

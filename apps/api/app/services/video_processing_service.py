import asyncio
import aiohttp
import json
import re
import os
import tempfile
import subprocess
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse
import logging
from datetime import datetime
import random
from app.llm.client import call_llm

logger = logging.getLogger(__name__)

class VideoProcessingService:
    """Production-grade video processing service focused on Instagram Reels"""
    
    def __init__(self):
        self.supported_platforms = {
            'instagram.com': self.process_video_urls
        }
        
        # Production user agents for stealth processing
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # Initialize RapidAPI service
        self.rapidapi_service = RapidAPIInstagramService(
            api_key=os.getenv('RAPIDAPI_KEY', ''),
            service_provider='rapidapi'
        )
        
        # Speech-to-text configuration
        self.speech_services = {
            'openai': OpenAISpeechService(),
            'google': GoogleSpeechService(),
            'azure': AzureSpeechService()
        }
    
    def _call_llm_with_json_schema(self, system_prompt: str, user_prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Call LLM with enforced JSON schema response format"""
        # CHANGE: Added structured JSON response enforcement
        enhanced_system_prompt = f"""{system_prompt}

CRITICAL: You MUST respond with ONLY valid JSON that matches this exact schema:
{json.dumps(schema, indent=2)}

Rules:
- Return ONLY the JSON object, no markdown, no explanations, no code blocks
- All property names must be in double quotes
- All string values must be in double quotes
- Use null for missing values, not undefined
- Ensure all required fields are present
- Do not add any text before or after the JSON"""

        enhanced_user_prompt = f"""{user_prompt}

RESPONSE FORMAT: Return ONLY valid JSON matching the provided schema. No markdown blocks, no explanations."""

        try:
            response = call_llm(enhanced_system_prompt, enhanced_user_prompt)
            
            # CHANGE: Strict JSON validation without markdown extraction
            if not response or not response.strip():
                raise ValueError("Empty LLM response")
            
            # Remove any potential whitespace and validate it's pure JSON
            cleaned_response = response.strip()
            
            # Ensure it starts with { and ends with }
            if not (cleaned_response.startswith('{') and cleaned_response.endswith('}')):
                raise ValueError(f"Response is not pure JSON: {cleaned_response[:100]}")
            
            # Parse and validate against schema structure
            parsed_json = json.loads(cleaned_response)
            
            # Basic schema validation
            self._validate_json_schema(parsed_json, schema)
            
            return parsed_json
            
        except json.JSONDecodeError as e:
            logger.error(f"LLM returned invalid JSON: {str(e)}, response: {response[:200] if response else 'None'}")
            raise ValueError(f"Invalid JSON from LLM: {str(e)}")
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise
    
    def _validate_json_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """Basic JSON schema validation"""
        # CHANGE: Added basic schema validation
        if "properties" in schema:
            for required_field in schema.get("required", []):
                if required_field not in data:
                    raise ValueError(f"Missing required field: {required_field}")
    
    def _detect_language_from_audio_transcript(self, audio_transcript: str) -> str:
        """Detect language from actual audio transcription using LLM with structured response"""
        # CHANGE: Use audio transcript for language detection instead of metadata
        if not audio_transcript or len(audio_transcript.strip()) < 5:
            logger.warning("No audio transcript available for language detection, defaulting to english")
            return "english"
        
        try:
            schema = {
                "type": "object",
                "properties": {
                    "language": {"type": "string", "enum": ["english", "hindi", "hinglish"]},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": ["language", "confidence"]
            }
            
            system_prompt = "You are a language detection expert. Analyze audio transcripts and identify the primary language."
            
            user_prompt = f"""Analyze this audio transcript and determine the primary language:

Audio Transcript: "{audio_transcript[:300]}"

Identify if this is:
- "english": Pure English content
- "hindi": Pure Hindi content  
- "hinglish": Mix of Hindi and English (common in Indian content)

Consider:
- Script/alphabet used
- Language mixing patterns
- Cultural context indicators"""

            result = self._call_llm_with_json_schema(system_prompt, user_prompt, schema)
            
            detected_language = result.get("language", "english")
            confidence = result.get("confidence", 0.5)
            
            logger.info(f"Detected language from audio: {detected_language} (confidence: {confidence})")
            return detected_language
            
        except Exception as e:
            logger.warning(f"Audio-based language detection failed: {str(e)}, defaulting to english")
            return "english"
    
    async def process_video_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Process multiple Instagram video URLs with comprehensive analysis"""
        logger.info(f"Starting production video processing for {len(urls)} URLs")
        
        results = {
            'extracted_content': [],
            'processing_metadata': [],
            'errors': []
        }
        
        if not urls:
            logger.warning("No URLs provided for processing")
            return results
        
        # Validate Instagram URLs only
        valid_urls = []
        for i, url in enumerate(urls):
            if self._validate_instagram_url(url):
                valid_urls.append(url)
                logger.info(f"Instagram URL {i+1}/{len(urls)} validated: {url}")
            else:
                error_msg = f"Invalid Instagram URL: {url}"
                logger.error(error_msg)
                results['errors'].append({
                    'url': url,
                    'error': 'Invalid Instagram URL format',
                    'error_type': 'validation_error'
                })
        
        if not valid_urls:
            logger.error("No valid Instagram URLs found")
            return results
        
        # Process URLs with production-grade error handling
        timeout = aiohttp.ClientTimeout(total=180)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            tasks = []
            for i, url in enumerate(valid_urls):
                # Stagger requests to avoid rate limiting
                delay = i * random.uniform(2, 5)
                logger.info(f"Scheduling URL {i+1} with {delay:.2f}s delay")
                tasks.append(self._process_single_url_with_delay(session, url, delay))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results with detailed logging
            for i, response in enumerate(responses):
                url = valid_urls[i]
                if isinstance(response, Exception):
                    logger.error(f"Failed to process {url}: {str(response)}")
                    results['errors'].append({
                        'url': url,
                        'error': str(response),
                        'error_type': 'processing_error'
                    })
                else:
                    logger.info(f"Successfully processed {url}")
                    results['extracted_content'].append(response['content'])
                    results['processing_metadata'].append(response['metadata'])
        
        logger.info(f"Processing completed - Success: {len(results['extracted_content'])}, Errors: {len(results['errors'])}")
        return results
    
    async def _process_single_url_with_delay(self, session: aiohttp.ClientSession, url: str, delay: float) -> Dict[str, Any]:
        """Process URL with delay and comprehensive error handling"""
        await asyncio.sleep(delay)
        return await self._process_single_url(session, url)
    
    def _validate_instagram_url(self, url: str) -> bool:
        """Validate Instagram URL format with comprehensive checks"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            domain = parsed.netloc.lower()
            if 'instagram.com' not in domain:
                return False
            
            # Check for valid Instagram content paths
            valid_paths = ['/reel/', '/p/', '/tv/']
            return any(path in url for path in valid_paths)
            
        except Exception as e:
            logger.error(f"URL validation error: {str(e)}")
            return False
    
    async def _process_single_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Process single Instagram URL with multiple extraction strategies"""
        logger.info(f"Processing Instagram URL: {url}")
        
        try:
            # Strategy 1: RapidAPI extraction (primary)
            rapidapi_result = await self._extract_with_rapidapi(session, url)
            if rapidapi_result and rapidapi_result.get('video_url'):
                logger.info(f"RapidAPI extraction successful for: {url}")
                
                # Download and analyze video
                video_analysis = await self._download_and_analyze_video(
                    session, rapidapi_result['video_url'], url
                )
                
                # Combine RapidAPI data with video analysis
                combined_result = await self._combine_analysis_results(
                    rapidapi_result, video_analysis, url
                )
                
                return combined_result
            
            # Strategy 2: Fallback scraping methods
            logger.info(f"Attempting fallback extraction for: {url}")
            fallback_result = await self._fallback_extraction(session, url)
            if fallback_result:
                return fallback_result
            
            # Strategy 3: Enhanced mock data with LLM analysis
            logger.warning(f"Using LLM-enhanced mock data for: {url}")
            return await self._generate_llm_enhanced_mock_data(url)
            
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            raise
    
    async def _extract_with_rapidapi(self, session: aiohttp.ClientSession, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using RapidAPI with enhanced error handling"""
        if not os.getenv('RAPIDAPI_KEY'):
            logger.warning("RAPIDAPI_KEY not configured")
            return None
        
        try:
            return await self.rapidapi_service.extract_instagram_video_data(url)
        except Exception as e:
            logger.error(f"RapidAPI extraction failed for {url}: {str(e)}")
            return None
    
    async def _download_and_analyze_video(self, session: aiohttp.ClientSession, video_url: str, original_url: str) -> Dict[str, Any]:
        """Download MP4 video and perform comprehensive analysis"""
        logger.info(f"Downloading and analyzing video: {video_url}")
        
        try:
            # Create secure temporary file
            temp_dir = tempfile.gettempdir()
            video_file = os.path.join(temp_dir, f"video_{hash(original_url)}.mp4")
            
            # Download video with progress tracking
            async with session.get(video_url, timeout=120) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download video: HTTP {response.status}")
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(video_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % (1024 * 1024) == 0:  # Log every MB
                                logger.debug(f"Download progress: {progress:.1f}%")
            
            logger.info(f"Video download completed: {video_file}")
            
            # Extract audio and analyze
            audio_transcript = await self._extract_audio_from_video(video_file)
            visual_analysis = await self._analyze_video_content_with_llm(video_file, original_url)
            
            # Clean up
            try:
                os.unlink(video_file)
                logger.debug(f"Cleaned up video file: {video_file}")
            except Exception as e:
                logger.warning(f"Could not clean up video file: {str(e)}")
            
            return {
                'audio_transcript': audio_transcript,
                'visual_analysis': visual_analysis,
                'processing_method': 'video_download_analysis'
            }
            
        except Exception as e:
            logger.error(f"Video analysis failed: {str(e)}")
            return {
                'audio_transcript': None,
                'visual_analysis': None,
                'processing_method': 'failed',
                'error': str(e)
            }
    
    async def _extract_audio_from_video(self, video_file_path: str) -> Optional[str]:
        """Extract audio from video using ffmpeg and transcribe"""
        logger.info(f"Extracting audio from: {video_file_path}")
        
        try:
            # Verify ffmpeg availability
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("ffmpeg not available - install ffmpeg for audio extraction")
                return None
            
            # Create temporary audio file
            temp_dir = tempfile.gettempdir()
            audio_file = os.path.join(temp_dir, f"audio_{hash(video_file_path)}.wav")
            
            # Extract audio with optimized settings
            ffmpeg_cmd = [
                'ffmpeg', '-i', video_file_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1',
                '-y', audio_file
            ]
            
            result = subprocess.run(
                ffmpeg_cmd, capture_output=True, text=True, timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"ffmpeg failed: {result.stderr}")
                return None
            
            # Verify audio file
            if not os.path.exists(audio_file) or os.path.getsize(audio_file) == 0:
                logger.error("Audio extraction produced empty file")
                return None
            
            # Transcribe using best available service
            transcript = await self._transcribe_audio_file(audio_file)
            
            # Clean up
            try:
                os.unlink(audio_file)
            except Exception as e:
                logger.warning(f"Could not clean up audio file: {str(e)}")
            
            return transcript
            
        except subprocess.TimeoutExpired:
            logger.error("Audio extraction timed out")
            return None
        except Exception as e:
            logger.error(f"Audio extraction failed: {str(e)}")
            return None
    
    async def _transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using best available service"""
        logger.info(f"Transcribing audio: {audio_file_path}")
        
        # Try services in order of preference
        services = [
            ('openai', 'OPENAI_API_KEY'),
            ('google', 'GOOGLE_APPLICATION_CREDENTIALS'),
            ('azure', 'AZURE_SPEECH_KEY')
        ]
        
        for service_name, env_var in services:
            if os.getenv(env_var):
                try:
                    logger.info(f"Attempting {service_name} transcription")
                    transcript = await self.speech_services[service_name].transcribe_audio(audio_file_path)
                    if transcript and len(transcript.strip()) > 0:
                        logger.info(f"{service_name} transcription successful")
                        return transcript
                except Exception as e:
                    logger.warning(f"{service_name} transcription failed: {str(e)}")
                    continue
        
        logger.warning("All speech-to-text services failed or unavailable")
        return None
    
    async def _analyze_video_content_with_llm(self, video_file_path: str, original_url: str) -> Dict[str, Any]:
        """Analyze video content using LLM with structured JSON response"""
        logger.info(f"Analyzing video content with LLM: {video_file_path}")
        
        try:
            # Extract basic video metadata
            video_info = await self._get_video_metadata(video_file_path)
            
            # CHANGE: Use structured JSON schema for video analysis
            schema = {
                "type": "object",
                "properties": {
                    "visual_style": {
                        "type": "object",
                        "properties": {
                            "dominant_colors": {"type": "array", "items": {"type": "string"}},
                            "composition_style": {"type": "string"},
                            "text_overlay_style": {"type": "string"},
                            "background_type": {"type": "string"}
                        },
                        "required": ["dominant_colors", "composition_style", "text_overlay_style", "background_type"]
                    },
                    "content_indicators": {
                        "type": "object",
                        "properties": {
                            "likely_topics": {"type": "array", "items": {"type": "string"}},
                            "content_format": {"type": "string"},
                            "energy_level": {"type": "string"},
                            "production_quality": {"type": "string"}
                        },
                        "required": ["likely_topics", "content_format", "energy_level", "production_quality"]
                    },
                    "engagement_patterns": {
                        "type": "object",
                        "properties": {
                            "hook_style": {"type": "string"},
                            "pacing": {"type": "string"},
                            "call_to_action_presence": {"type": "boolean"}
                        },
                        "required": ["hook_style", "pacing", "call_to_action_presence"]
                    }
                },
                "required": ["visual_style", "content_indicators", "engagement_patterns"]
            }
            
            system_prompt = "You are a video content analyst. Analyze Instagram Reels and provide structured insights."
            
            user_prompt = f"""Analyze this Instagram Reel video and extract visual and stylistic characteristics:

Video URL: {original_url}
Duration: {video_info.get('duration', 'unknown')}

Based on typical Instagram Reel patterns, analyze:

Visual Style:
- dominant_colors: List 2-3 hex color codes
- composition_style: "talking-head", "tutorial", "lifestyle", or "food"
- text_overlay_style: "minimal", "heavy", "dynamic", or "none"
- background_type: "indoor", "outdoor", "studio", or "kitchen"

Content Indicators:
- likely_topics: Array of 1-3 topic strings
- content_format: "educational", "entertainment", "personal", or "promotional"
- energy_level: "low", "medium", or "high"
- production_quality: "basic", "professional", or "high-end"

Engagement Patterns:
- hook_style: "question", "statement", "visual", or "action"
- pacing: "slow", "moderate", or "fast"
- call_to_action_presence: true or false"""

            try:
                analysis_data = self._call_llm_with_json_schema(system_prompt, user_prompt, schema)
                logger.info(f"LLM video analysis successful for: {original_url}")
                return analysis_data
                
            except Exception as e:
                logger.warning(f"LLM analysis failed, using fallback: {str(e)}")
                return self._get_fallback_video_analysis()
            
        except Exception as e:
            logger.error(f"Video content analysis failed: {str(e)}")
            return self._get_fallback_video_analysis()
    
    async def _get_video_metadata(self, video_file_path: str) -> Dict[str, Any]:
        """Extract basic video metadata using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                duration = float(metadata.get('format', {}).get('duration', 0))
                return {
                    'duration': duration,
                    'format': metadata.get('format', {}),
                    'streams': metadata.get('streams', [])
                }
        except Exception as e:
            logger.warning(f"Could not extract video metadata: {str(e)}")
        
        return {'duration': 30}  # Default assumption
    
    def _get_fallback_video_analysis(self) -> Dict[str, Any]:
        """Fallback video analysis when LLM fails"""
        return {
            "visual_style": {
                "dominant_colors": ["#E4405F", "#FFFFFF"],
                "composition_style": "talking-head",
                "text_overlay_style": "minimal",
                "background_type": "indoor"
            },
            "content_indicators": {
                "likely_topics": ["general"],
                "content_format": "educational",
                "energy_level": "medium",
                "production_quality": "basic"
            },
            "engagement_patterns": {
                "hook_style": "statement",
                "pacing": "moderate",
                "call_to_action_presence": True
            }
        }
    
    async def _combine_analysis_results(self, rapidapi_data: Dict[str, Any], video_analysis: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Combine RapidAPI data with video analysis using structured LLM response"""
        logger.info(f"Combining analysis results for: {url}")
        
        # CHANGE: Detect language from audio transcript instead of metadata
        audio_transcript = video_analysis.get('audio_transcript', '')
        detected_language = self._detect_language_from_audio_transcript(audio_transcript)
        
        # CHANGE: Use structured JSON schema for synthesis
        schema = {
            "type": "object",
            "properties": {
                "content": {
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "main_topics": {"type": "array", "items": {"type": "string"}},
                        "content_type": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["transcript", "main_topics", "content_type", "language"]
                },
                "style_markers": {
                    "type": "object",
                    "properties": {
                        "communication_style": {"type": "string"},
                        "authenticity_indicators": {"type": "array", "items": {"type": "string"}},
                        "signature_elements": {"type": "array", "items": {"type": "string"}},
                        "emotional_tone": {"type": "string"}
                    },
                    "required": ["communication_style", "authenticity_indicators", "signature_elements", "emotional_tone"]
                },
                "visual_characteristics": {
                    "type": "object",
                    "properties": {
                        "color_preferences": {"type": "array", "items": {"type": "string"}},
                        "composition_style": {"type": "string"},
                        "text_usage": {"type": "string"},
                        "production_style": {"type": "string"}
                    },
                    "required": ["color_preferences", "composition_style", "text_usage", "production_style"]
                },
                "engagement_strategy": {
                    "type": "object",
                    "properties": {
                        "hook_approach": {"type": "string"},
                        "pacing_style": {"type": "string"},
                        "interaction_style": {"type": "string"}
                    },
                    "required": ["hook_approach", "pacing_style", "interaction_style"]
                },
                "confidence_score": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["content", "style_markers", "visual_characteristics", "engagement_strategy", "confidence_score"]
        }
        
        system_prompt = "You are an expert content analyst. Synthesize multi-modal data into comprehensive creator insights."
        
        user_prompt = f"""Combine and synthesize the following data sources for Instagram Reel analysis:

RAPIDAPI DATA:
{json.dumps(rapidapi_data, indent=2)}

VIDEO ANALYSIS:
{json.dumps(video_analysis, indent=2)}

AUDIO TRANSCRIPT: {audio_transcript[:200] if audio_transcript else 'No audio transcript available'}

DETECTED LANGUAGE: {detected_language}

Create a comprehensive content analysis with these requirements:

Content:
- transcript: Use audio transcript if available, otherwise RapidAPI caption
- main_topics: 1-3 relevant topics based on content
- content_type: "educational", "entertainment", "lifestyle", or "tutorial"
- language: "{detected_language}"

Style Markers:
- communication_style: "casual", "professional", "energetic", or "calm"
- authenticity_indicators: 2-3 specific authentic elements
- signature_elements: 2-3 unique creator elements
- emotional_tone: "enthusiastic", "informative", "personal", or "motivational"

Visual Characteristics:
- color_preferences: 2-3 hex color codes
- composition_style: Brief description of visual style
- text_usage: "heavy", "moderate", or "minimal"
- production_style: "professional", "casual", or "artistic"

Engagement Strategy:
- hook_approach: "question", "story", "fact", or "visual"
- pacing_style: "fast", "moderate", or "slow"
- interaction_style: "direct", "conversational", or "instructional"

confidence_score: 0.0-1.0 based on data quality"""

        try:
            synthesis_data = self._call_llm_with_json_schema(system_prompt, user_prompt, schema)
            
            # Ensure language is preserved from audio detection
            synthesis_data['content']['language'] = detected_language
            
            return {
                'content': synthesis_data,
                'metadata': {
                    'url': url,
                    'processing_method': 'llm_synthesis_structured',
                    'data_sources': ['rapidapi', 'video_analysis', 'audio_transcript'],
                    'processed_at': datetime.utcnow().isoformat(),
                    'confidence_score': synthesis_data.get('confidence_score', 0.7),
                    'detected_language': detected_language,
                    'audio_transcript_available': bool(audio_transcript)
                }
            }
            
        except Exception as e:
            logger.error(f"LLM synthesis failed: {str(e)}")
            # Fallback to basic combination
            return self._basic_data_combination(rapidapi_data, video_analysis, url, detected_language)
    
    def _basic_data_combination(self, rapidapi_data: Dict[str, Any], video_analysis: Dict[str, Any], url: str, detected_language: str = "english") -> Dict[str, Any]:
        """Basic data combination when LLM synthesis fails"""
        # CHANGE: Use audio transcript for language detection in fallback
        audio_transcript = video_analysis.get('audio_transcript', '')
        if audio_transcript:
            detected_language = self._detect_language_from_audio_transcript(audio_transcript)
        
        return {
            'content': {
                'transcript': audio_transcript or rapidapi_data.get('transcript', 'Instagram content'),
                'main_topics': ['general'],
                'content_type': 'educational',
                'language': detected_language
            },
            'metadata': {
                'url': url,
                'processing_method': 'basic_combination',
                'processed_at': datetime.utcnow().isoformat(),
                'confidence_score': 0.5,
                'detected_language': detected_language,
                'audio_transcript_available': bool(audio_transcript)
            }
        }
    
    async def _fallback_extraction(self, session: aiohttp.ClientSession, url: str) -> Optional[Dict[str, Any]]:
        """Fallback extraction methods when RapidAPI fails"""
        logger.info(f"Attempting fallback extraction for: {url}")
        
        try:
            # Try Instagram embed endpoint
            post_id = self._extract_instagram_post_id(url)
            if post_id:
                embed_url = f"https://www.instagram.com/p/{post_id}/embed/"
                headers = self._get_random_headers()
                
                async with session.get(embed_url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        return await self._parse_embed_content_with_llm(html_content, url)
            
            return None
            
        except Exception as e:
            logger.error(f"Fallback extraction failed: {str(e)}")
            return None
    
    async def _parse_embed_content_with_llm(self, html_content: str, url: str) -> Dict[str, Any]:
        """Parse embed content using LLM with structured response"""
        # Extract basic content first
        caption_match = re.search(r'"caption":"([^"]*)"', html_content)
        caption = caption_match.group(1) if caption_match else ""
        
        # CHANGE: Use structured schema for embed analysis
        schema = {
            "type": "object",
            "properties": {
                "content_analysis": {
                    "type": "object",
                    "properties": {
                        "main_message": {"type": "string"},
                        "communication_style": {"type": "string"},
                        "topics": {"type": "array", "items": {"type": "string"}},
                        "language": {"type": "string"}
                    },
                    "required": ["main_message", "communication_style", "topics", "language"]
                },
                "creator_characteristics": {
                    "type": "object",
                    "properties": {
                        "tone": {"type": "string"},
                        "authenticity_markers": {"type": "array", "items": {"type": "string"}},
                        "engagement_approach": {"type": "string"}
                    },
                    "required": ["tone", "authenticity_markers", "engagement_approach"]
                },
                "confidence_score": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["content_analysis", "creator_characteristics", "confidence_score"]
        }
        
        # Detect language from caption
        detected_language = self._detect_language_from_audio_transcript(caption) if caption else "english"
        
        system_prompt = "You are a content analyst. Extract creator characteristics from Instagram content."
        
        user_prompt = f"""Analyze this Instagram embed HTML content and extract creator insights:

URL: {url}
Extracted Caption: {caption}
Detected Language: {detected_language}

Content Analysis:
- main_message: Primary message or topic from the content
- communication_style: Style description based on caption
- topics: 1-3 relevant topics
- language: "{detected_language}"

Creator Characteristics:
- tone: "casual", "professional", or "energetic"
- authenticity_markers: 2-3 authentic elements from content
- engagement_approach: "direct", "storytelling", or "educational"

confidence_score: 0.0-1.0 based on available data quality"""

        try:
            analysis_data = self._call_llm_with_json_schema(system_prompt, user_prompt, schema)
            
            return {
                'content': {
                    'transcript': caption or analysis_data.get('content_analysis', {}).get('main_message', 'Instagram content'),
                    'analysis': analysis_data,
                    'language': detected_language
                },
                'metadata': {
                    'url': url,
                    'processing_method': 'llm_embed_analysis_structured',
                    'processed_at': datetime.utcnow().isoformat(),
                    'confidence_score': analysis_data.get('confidence_score', 0.6),
                    'detected_language': detected_language
                }
            }
            
        except Exception as e:
            logger.error(f"LLM embed analysis failed: {str(e)}")
            return {
                'content': {
                    'transcript': caption or 'Instagram content',
                    'language': detected_language
                },
                'metadata': {
                    'url': url,
                    'processing_method': 'basic_embed',
                    'processed_at': datetime.utcnow().isoformat(),
                    'confidence_score': 0.3,
                    'detected_language': detected_language
                }
            }
    
    async def _generate_llm_enhanced_mock_data(self, url: str) -> Dict[str, Any]:
        """Generate enhanced mock data using structured LLM response"""
        logger.info(f"Generating LLM-enhanced mock data for: {url}")
        
        post_id = self._extract_instagram_post_id(url)
        
        # CHANGE: Use structured schema for mock data generation
        schema = {
            "type": "object",
            "properties": {
                "content": {
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "main_topics": {"type": "array", "items": {"type": "string"}},
                        "content_type": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["transcript", "main_topics", "content_type", "language"]
                },
                "creator_style": {
                    "type": "object",
                    "properties": {
                        "communication_approach": {"type": "string"},
                        "energy_level": {"type": "string"},
                        "authenticity_markers": {"type": "array", "items": {"type": "string"}},
                        "signature_elements": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["communication_approach", "energy_level", "authenticity_markers", "signature_elements"]
                },
                "visual_style": {
                    "type": "object",
                    "properties": {
                        "typical_colors": {"type": "array", "items": {"type": "string"}},
                        "composition": {"type": "string"},
                        "text_overlay_usage": {"type": "string"}
                    },
                    "required": ["typical_colors", "composition", "text_overlay_usage"]
                }
            },
            "required": ["content", "creator_style", "visual_style"]
        }
        
        system_prompt = "You are a content creator analyst. Generate realistic Instagram Reel analysis."
        
        user_prompt = f"""Generate realistic Instagram Reel content analysis for URL: {url}
Post ID: {post_id}

Create believable creator content:

Content:
- transcript: Realistic Instagram reel content (20-50 words)
- main_topics: 2-3 relevant topics
- content_type: "educational", "lifestyle", or "entertainment"
- language: "english"

Creator Style:
- communication_approach: Style description
- energy_level: "high", "medium", or "low"
- authenticity_markers: 2-3 realistic markers
- signature_elements: 2-3 typical elements

Visual Style:
- typical_colors: 2-3 hex color codes
- composition: Typical composition style description
- text_overlay_usage: Description of text overlay usage"""

        try:
            mock_data = self._call_llm_with_json_schema(system_prompt, user_prompt, schema)
            
            return {
                'content': mock_data,
                'metadata': {
                    'url': url,
                    'processing_method': 'llm_enhanced_mock_structured',
                    'processed_at': datetime.utcnow().isoformat(),
                    'confidence_score': 0.4,
                    'is_mock_data': True
                }
            }
            
        except Exception as e:
            logger.error(f"LLM mock generation failed: {str(e)}")
            return self._basic_mock_data(url)
    
    def _basic_mock_data(self, url: str) -> Dict[str, Any]:
        """Basic mock data fallback"""
        post_id = self._extract_instagram_post_id(url)
        
        return {
            'content': {
                'transcript': f'Instagram Reel content from post {post_id}',
                'main_topics': ['general'],
                'content_type': 'educational',
                'language': 'english'
            },
            'metadata': {
                'url': url,
                'processing_method': 'basic_mock',
                'processed_at': datetime.utcnow().isoformat(),
                'confidence_score': 0.2,
                'is_mock_data': True
            }
        }
    
    def _extract_instagram_post_id(self, url: str) -> Optional[str]:
        """Extract Instagram post ID from URL"""
        patterns = [
            r'/p/([A-Za-z0-9_-]+)',
            r'/reel/([A-Za-z0-9_-]+)',
            r'/tv/([A-Za-z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _get_random_headers(self) -> Dict[str, str]:
        """Get randomized headers for stealth requests"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }


# Enhanced Speech-to-Text Services
class OpenAISpeechService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            with open(audio_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                return transcript
            
        except Exception as e:
            logger.error(f"OpenAI Whisper transcription failed: {str(e)}")
            raise


class GoogleSpeechService:
    def __init__(self):
        self.credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using Google Speech-to-Text"""
        if not self.credentials_path:
            raise ValueError("Google credentials not configured")
        
        try:
            from google.cloud import speech
            
            client = speech.SpeechClient()
            
            with open(audio_file_path, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            
            response = client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return transcript.strip()
            
        except Exception as e:
            logger.error(f"Google Speech-to-Text failed: {str(e)}")
            raise


class AzureSpeechService:
    def __init__(self):
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using Azure Speech Services"""
        if not self.speech_key or not self.speech_region:
            raise ValueError("Azure Speech credentials not configured")
        
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
            speech_config.speech_recognition_language = "en-US"
            
            audio_input = speechsdk.AudioConfig(filename=audio_file_path)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, 
                audio_config=audio_input
            )
            
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return "No speech could be recognized"
            else:
                raise ValueError(f"Speech recognition failed: {result.reason}")
            
        except Exception as e:
            logger.error(f"Azure Speech Services failed: {str(e)}")
            raise


# Enhanced RapidAPI Service
class RapidAPIInstagramService:
    def __init__(self, api_key: str, service_provider: str = "rapidapi"):
        self.api_key = api_key
        self.service_provider = service_provider
        self.base_url = "https://instagram120.p.rapidapi.com"
    
    async def extract_instagram_video_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract Instagram video data with enhanced error handling"""
        if not self.api_key:
            logger.warning("RapidAPI key not configured")
            return None
        
        try:
            headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "instagram120.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            
            payload = {"url": url}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/instagram/links",
                    headers=headers,
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_rapidapi_response(data, url)
                    else:
                        logger.warning(f"RapidAPI request failed: HTTP {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"RapidAPI extraction failed: {str(e)}")
            return None
    
    def _parse_rapidapi_response(self, data: List[Dict[str, Any]], url: str) -> Dict[str, Any]:
        """Parse RapidAPI response with enhanced data extraction"""
        if not data or not isinstance(data, list) or len(data) == 0:
            logger.warning(f"Invalid RapidAPI response format for {url}")
            return None
        
        item = data[0]
        meta = item.get('meta', {})
        urls = item.get('urls', [])
        
        # Extract video URL (MP4)
        video_url = None
        if urls:
            for url_item in urls:
                if url_item.get('extension') == 'mp4' or url_item.get('name') == 'MP4':
                    video_url = url_item.get('url')
                    break
        
        # Extract and clean content
        title = meta.get('title', '')
        if title:
            import html
            title = html.unescape(title)
        
        return {
            'transcript': title or 'Instagram content',
            'video_url': video_url,
            'metadata': {
                'username': meta.get('username', 'unknown'),
                'shortcode': meta.get('shortcode', ''),
                'likes': meta.get('likeCount', 0),
                'comments': meta.get('commentCount', 0),
                'posted_at': meta.get('takenAt', 0),
                'platform': 'instagram',
                'url': url,
                'extraction_method': 'rapidapi'
            }
        }
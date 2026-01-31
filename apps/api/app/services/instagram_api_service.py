import aiohttp
import json
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class InstagramAPIService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com"
    
    async def get_media_data(self, media_id: str) -> Dict[str, Any]:
        """Get media data using Instagram Basic Display API"""
        try:
            url = f"{self.base_url}/{media_id}"
            params = {
                'fields': 'id,media_type,media_url,permalink,timestamp,caption',
                'access_token': self.access_token
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'transcript': data.get('caption', ''),
                            'metadata': {
                                'title': 'Instagram Media',
                                'duration': 30,  # Estimate for reels
                                'platform': 'instagram',
                                'url': data.get('permalink'),
                                'extracted_at': datetime.utcnow().isoformat(),
                                'api_source': True
                            },
                            'visual_data': {
                                'media_url': data.get('media_url'),
                                'media_type': data.get('media_type'),
                                'scene_composition': 'api-extracted'
                            }
                        }
                    else:
                        raise Exception(f"API request failed: {response.status}")
        except Exception as e:
            logger.error(f"Instagram API error: {str(e)}")
            raise
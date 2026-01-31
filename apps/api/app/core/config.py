import os
import socket
import urllib.parse
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def database_url_with_fallback(self) -> str:
        """Get database URL with network-aware fallback"""
        if not self.DATABASE_URL:
            logger.warning("DATABASE_URL not set, using SQLite fallback")
            return "sqlite:///./creator_ai_local.db"
        
        # In development, test connectivity before using PostgreSQL
        if self.ENVIRONMENT == "development" and self.DATABASE_URL.startswith("postgresql://"):
            if not self._test_database_connectivity():
                logger.warning("PostgreSQL unreachable, falling back to SQLite")
                return "sqlite:///./creator_ai_local.db"
        
        return self.DATABASE_URL
    
    def _test_database_connectivity(self) -> bool:
        """Test if database server is reachable"""
        try:
            parsed = urllib.parse.urlparse(self.DATABASE_URL)
            host = parsed.hostname
            port = parsed.port or 5432
            
            logger.info(f"Testing connectivity to {host}:{port}")
            
            # Quick connectivity test with short timeout
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"✅ Network connectivity to {host}:{port} successful")
                return True
            else:
                logger.warning(f"❌ Cannot reach {host}:{port} (error code: {result})")
                return False
            
        except Exception as e:
            logger.warning(f"Connectivity test failed: {e}")
            return False
    
    def validate(self):
        """Validate required settings"""
        if self.ENVIRONMENT == "production" and not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required in production environment")

settings = Settings()
settings.validate()
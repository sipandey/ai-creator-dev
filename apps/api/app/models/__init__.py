# Import models in dependency order to avoid circular imports
from app.core.database import Base

# Base models first
from .user import User

# Dependent models
from .persona import CreatorPersona
from .feedback import Feedback
from .preference import Preference
from .content_source import ContentSource
from .script import Script
from .strategy import ContentStrategy

# Make sure all models are available for alembic
__all__ = [
    "Base",
    "User", 
    "CreatorPersona",
    "Feedback", 
    "Preference",
    "ContentSource",
    "Script",
    "ContentStrategy"
]

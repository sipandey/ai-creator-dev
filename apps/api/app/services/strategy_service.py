from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.strategy import ContentStrategy
from app.models.persona import CreatorPersona
from app.agents.strategy_agent import generate_weekly_plan as generate_weekly_strategy
from app.services.preference_service import load_preferences
import logging

logger = logging.getLogger(__name__)

class StrategyService:
    """Service for managing content strategy generation and invalidation"""

    def __init__(self, db: Session):
        self.db = db

    def regenerate_weekly_strategy(self, user_id: int) -> dict:
        """Regenerate the current week's strategy for a user"""
        logger.info(f"Regenerating weekly strategy for user {user_id}")

        # Calculate start of current week (Monday)
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

        # Get persona and preferences
        persona = (
            self.db.query(CreatorPersona)
            .filter(CreatorPersona.user_id == user_id)
            .first()
        )

        if not persona:
            raise ValueError(f"No persona found for user {user_id}")

        prefs = load_preferences(self.db, user_id)

        # Generate new strategy
        strategy_data = generate_weekly_strategy(
            persona.persona_json,
            prefs
        )

        # Update or create strategy record
        existing_strategy = (
            self.db.query(ContentStrategy)
            .filter(
                ContentStrategy.user_id == user_id,
                ContentStrategy.week_start_date == start_of_week
            )
            .first()
        )

        if existing_strategy:
            logger.info(f"Updating existing strategy for user {user_id}")
            existing_strategy.strategy_json = strategy_data
        else:
            logger.info(f"Creating new strategy for user {user_id}")
            new_strategy = ContentStrategy(
                user_id=user_id,
                week_start_date=start_of_week,
                strategy_json=strategy_data
            )
            self.db.add(new_strategy)

        self.db.commit()
        logger.info(f"Strategy regeneration completed for user {user_id}")

        return strategy_data

    def invalidate_strategy_on_persona_change(self, user_id: int) -> None:
        """Mark current week's strategy as invalid when persona changes"""
        logger.info(f"Invalidating strategy for user {user_id} due to persona change")

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

        # Delete current week's strategy to force regeneration
        deleted_count = (
            self.db.query(ContentStrategy)
            .filter(
                ContentStrategy.user_id == user_id,
                ContentStrategy.week_start_date == start_of_week
            )
            .delete()
        )

        if deleted_count > 0:
            logger.info(f"Invalidated {deleted_count} strategy record(s) for user {user_id}")
        else:
            logger.info(f"No strategy found to invalidate for user {user_id}")

        self.db.commit()
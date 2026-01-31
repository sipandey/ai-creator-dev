from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.deps import get_db, get_current_user
from app.models.persona import CreatorPersona
from app.models.strategy import ContentStrategy
from app.agents.strategy_agent import generate_weekly_plan as generate_weekly_strategy
from app.services.preference_service import load_preferences
from app.services.strategy_service import StrategyService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/strategy")

@router.get("/weekly")
def get_weekly_strategy(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    # Calculate start of current week (Monday)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    # Check if strategy exists for this week
    existing_strategy = (
        db.query(ContentStrategy)
        .filter(
            ContentStrategy.user_id == user.id,
            ContentStrategy.week_start_date == start_of_week
        )
        .first()
    )

    if existing_strategy:
        return existing_strategy.strategy_json

    # If not, generate new one
    persona = (
        db.query(CreatorPersona)
        .filter(CreatorPersona.user_id == user.id)
        .first()
    )

    prefs = load_preferences(db, user.id)

    strategy_data = generate_weekly_strategy(
        persona.persona_json,
        prefs
    )

    # Save to DB
    new_strategy = ContentStrategy(
        user_id=user.id,
        week_start_date=start_of_week,
        strategy_json=strategy_data
    )
    db.add(new_strategy)
    db.commit()

    return strategy_data

@router.post("/generate")
def force_generate_weekly_plan(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """Force generate a new strategy for the current week (overwrite)"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    persona = (
        db.query(CreatorPersona)
        .filter(CreatorPersona.user_id == user.id)
        .first()
    )

    prefs = load_preferences(db, user.id)

    strategy_data = generate_weekly_strategy(
        persona.persona_json,
        prefs
    )

    # Check if exists to update or create
    existing_strategy = (
        db.query(ContentStrategy)
        .filter(
            ContentStrategy.user_id == user.id,
            ContentStrategy.week_start_date == start_of_week
        )
        .first()
    )

    if existing_strategy:
        existing_strategy.strategy_json = strategy_data
    else:
        new_strategy = ContentStrategy(
            user_id=user.id,
            week_start_date=start_of_week,
            strategy_json=strategy_data
        )
        db.add(new_strategy)

    db.commit()

    return strategy_data

@router.post("/invalidate")
def invalidate_weekly_strategy(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """Invalidate current week's strategy (will be regenerated on next request)"""
    strategy_service = StrategyService(db)
    strategy_service.invalidate_strategy_on_persona_change(user.id)
    
    return {"message": "Strategy invalidated. Will be regenerated on next request."}

@router.post("/regenerate")
def force_regenerate_weekly_strategy(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """Force regenerate the current week's strategy"""
    strategy_service = StrategyService(db)
    strategy_data = strategy_service.regenerate_weekly_strategy(user.id)
    
    return strategy_data

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.services.persona_service import upsert_persona, get_personas
from app.services.strategy_service import StrategyService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persona")


@router.get("")
def read_personas(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return get_personas(db=db, user_id=user.id)


@router.post("")
def save_persona(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),  # 👈 THIS IS THE KEY
):
    result = upsert_persona(
        db=db,
        user_id=user.id,  # 👈 real logged-in user
        persona=payload,
        confidence=0.7,
        source="template",
    )

    # Regenerate strategy after persona save
    try:
        logger.info(f"Regenerating strategy for user {user.id} after persona save")
        strategy_service = StrategyService(db)
        strategy_service.regenerate_weekly_strategy(user.id)
    except Exception as e:
        logger.error(f"Failed to regenerate strategy after save for user {user.id}: {str(e)}")
        # Don't fail the save if strategy regeneration fails

    return result

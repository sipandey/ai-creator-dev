from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.services.persona_builder import build_persona
from app.services.persona_service import upsert_persona
from app.services.strategy_service import StrategyService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persona/build")

@router.post("")
def build_creator_persona(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    persona, confidence, source = build_persona(user.creator_type, payload)

    result = upsert_persona(
        db=db,
        user_id=user.id,
        persona=persona,
        confidence=confidence,
        source=source,
    )

    # Regenerate strategy after persona build
    try:
        logger.info(f"Regenerating strategy for user {user.id} after persona build")
        strategy_service = StrategyService(db)
        strategy_service.regenerate_weekly_strategy(user.id)
    except Exception as e:
        logger.error(f"Failed to regenerate strategy after build for user {user.id}: {str(e)}")
        # Don't fail the build if strategy regeneration fails

    return result

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.persona import CreatorPersona
from app.models.feedback import Feedback
from app.services.persona_refinement_service import apply_feedback
from app.services.strategy_service import StrategyService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persona/refine")

@router.post("")
def refine_persona_api(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    persona_row = (
        db.query(CreatorPersona)
        .filter(CreatorPersona.user_id == user.id)
        .first()
    )

    feedback = (
        db.query(Feedback)
        .filter(Feedback.user_id == user.id)
        .all()
    )

    refined = apply_feedback(
        persona_row.persona_json,
        [f.__dict__ for f in feedback],
    )

    persona_row.persona_json = refined
    persona_row.confidence_score = min(
        persona_row.confidence_score + 0.05, 1.0
    )

    db.commit()

    # Regenerate strategy after persona refinement
    try:
        logger.info(f"Regenerating strategy for user {user.id} after persona refinement")
        strategy_service = StrategyService(db)
        strategy_service.regenerate_weekly_strategy(user.id)
    except Exception as e:
        logger.error(f"Failed to regenerate strategy after refinement for user {user.id}: {str(e)}")
        # Don't fail the refinement if strategy regeneration fails

    return refined
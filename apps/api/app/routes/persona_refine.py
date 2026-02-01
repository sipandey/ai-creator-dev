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

    # Persona refinement always changes the persona, so invalidate strategy
    try:
        logger.info(f"Persona refined for user {user.id}, invalidating strategy and scripts")
        strategy_service = StrategyService(db)
        strategy_service.invalidate_strategy_on_persona_change(user.id)

        # Also invalidate any draft scripts since persona changed
        from app.models.script import Script, ScriptStatus
        deleted_scripts = (
            db.query(Script)
            .filter(
                Script.user_id == user.id,
                Script.status == ScriptStatus.DRAFT
            )
            .delete()
        )
        if deleted_scripts > 0:
            logger.info(f"Invalidated {deleted_scripts} draft scripts for user {user.id}")
        db.commit()
    except Exception as e:
        logger.error(f"Failed to invalidate content after persona refinement for user {user.id}: {str(e)}")
        # Don't fail the refinement if strategy regeneration fails

    return refined
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
    result, persona_changed = upsert_persona(
        db=db,
        user_id=user.id,  # 👈 real logged-in user
        persona=payload,
        confidence=0.7,
        source="template",
    )

    # Only regenerate strategy if persona actually changed
    if persona_changed:
        try:
            logger.info(f"Persona changed for user {user.id}, invalidating strategy and scripts")
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
            logger.error(f"Failed to invalidate content after persona change for user {user.id}: {str(e)}")
            # Don't fail the save if invalidation fails

    return result

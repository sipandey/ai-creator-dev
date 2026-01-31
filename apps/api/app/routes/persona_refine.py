from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.persona import CreatorPersona
from app.models.feedback import Feedback
from app.services.persona_refinement_service import apply_feedback

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

    return refined
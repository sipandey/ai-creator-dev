from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.feedback import Feedback

router = APIRouter(prefix="/feedback")

@router.post("")
def submit_feedback(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    feedback = Feedback(
        user_id=user.id,
        target=payload.get("target"),
        feedback_type=payload.get("type"),
        signal=payload.get("signal"),
        comment=payload.get("comment"),
    )

    db.add(feedback)
    db.commit()

    return {"status": "recorded"}

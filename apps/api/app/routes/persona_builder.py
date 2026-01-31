from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.services.persona_builder import build_persona
from app.services.persona_service import upsert_persona

router = APIRouter(prefix="/persona/build")

@router.post("")
def build_creator_persona(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    persona, confidence, source = build_persona(user.creator_type, payload)

    return upsert_persona(
        db=db,
        user_id=user.id,
        persona=persona,
        confidence=confidence,
        source=source,
    )

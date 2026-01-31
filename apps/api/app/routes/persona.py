from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.services.persona_service import upsert_persona, get_personas

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
    return upsert_persona(
        db=db,
        user_id=user.id,  # 👈 real logged-in user
        persona=payload,
        confidence=0.7,
        source="template",
    )

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.preference import Preference

router = APIRouter(prefix="/preferences")

@router.post("")
def set_preference(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    pref = Preference(
        user_id=user.id,
        key=payload["key"],
        type=payload["type"],
        value=str(payload["value"]),
        confidence=payload.get("confidence", 0.5),
    )

    db.add(pref)
    db.commit()

    return {"status": "saved"}

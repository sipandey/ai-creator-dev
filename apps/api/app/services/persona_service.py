from sqlalchemy.orm import Session
from app.models.persona import CreatorPersona
import json


def get_personas(db: Session, user_id: int):
    return db.query(CreatorPersona).filter(CreatorPersona.user_id == user_id).all()


def upsert_persona(
    db: Session,
    user_id: int,
    persona: dict,
    confidence: float,
    source: str,
):
    """
    Create or update a creator persona for a given user.

    - If persona already exists for the user → update it
    - Else → create a new persona record

    Returns: (persona_record, was_changed)
    """

    # 1️⃣ Check if persona already exists for this user
    existing_persona = (
        db.query(CreatorPersona)
        .filter(CreatorPersona.user_id == user_id)
        .first()
    )

    # 2️⃣ If exists → check if data actually changed
    if existing_persona:
        # Compare persona data (excluding timestamps and metadata)
        existing_data = existing_persona.persona_json
        new_data = persona

        # Simple comparison - check if the persona JSON changed
        persona_changed = json.dumps(existing_data, sort_keys=True) != json.dumps(new_data, sort_keys=True)

        if persona_changed or existing_persona.confidence_score != confidence or existing_persona.source != source:
            existing_persona.persona_json = persona
            existing_persona.confidence_score = confidence
            existing_persona.source = source

            db.commit()
            db.refresh(existing_persona)
            return existing_persona, True  # Changed
        else:
            return existing_persona, False  # No change

    # 3️⃣ Else → create new persona
    new_persona = CreatorPersona(
        user_id=user_id,
        persona_json=persona,
        confidence_score=confidence,
        source=source,
    )

    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)
    return new_persona, True  # Created (changed)

    return new_persona

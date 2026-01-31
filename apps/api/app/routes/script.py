from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.persona import CreatorPersona
from app.models.script import Script, ScriptStatus
from app.agents.script_agent import generate_script
from app.services.preference_service import load_preferences
from app.schemas.script import ScriptUpdate, ScriptResponse
import json

router = APIRouter(prefix="/script")

@router.post("", response_model=ScriptResponse)
def generate_reel_script(
    payload: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    topic = payload.get("topic")

    persona = (
        db.query(CreatorPersona)
        .filter(CreatorPersona.user_id == user.id)
        .first()
    )

    prefs = load_preferences(db, user.id)

    # Check if a DRAFT script already exists for this topic
    existing_script = (
        db.query(Script)
        .filter(
            Script.user_id == user.id,
            Script.topic == topic,
            Script.status == ScriptStatus.DRAFT
        )
        .first()
    )

    if existing_script:
        # If exists and is just a draft, return it instead of re-generating
        # Note: In a real app, you might want an option to 'regenerate' explicitly
        return existing_script

    generated_script = generate_script(
        persona.persona_json,
        topic,
        prefs
    )

    # Save draft script to DB
    new_script = Script(
        user_id=user.id,
        topic=topic,
        script_json=generated_script,
        status=ScriptStatus.DRAFT
    )
    db.add(new_script)
    db.commit()
    db.refresh(new_script)

    return new_script

@router.get("", response_model=list[ScriptResponse])
def get_scripts(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """List all scripts for the current user"""
    scripts = (
        db.query(Script)
        .filter(Script.user_id == user.id)
        .order_by(Script.updated_at.desc())
        .all()
    )
    return scripts

@router.get("/{script_id}", response_model=ScriptResponse)
def get_script(
    script_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """Get a specific script by ID"""
    script = (
        db.query(Script)
        .filter(Script.id == script_id, Script.user_id == user.id)
        .first()
    )
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    return script

@router.post("/{script_id}/status", response_model=ScriptResponse)
def update_script_status(
    script_id: int,
    payload: ScriptUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    script = (
        db.query(Script)
        .filter(Script.id == script_id, Script.user_id == user.id)
        .first()
    )

    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )

    script.status = payload.status
    if payload.performance_data:
        script.performance_data = payload.performance_data

    db.commit()
    db.refresh(script)

    return script

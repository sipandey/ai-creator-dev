from app.models.preference import Preference

def load_preferences(db, user_id: int) -> dict:
    prefs = db.query(Preference).filter(
        Preference.user_id == user_id
    ).all()

    hard = {}
    soft = {}

    for p in prefs:
        if p.type == "hard":
            hard[p.key] = p.value
        else:
            soft[p.key] = {
                "value": p.value,
                "confidence": p.confidence,
            }

    return {
        "hard": hard,
        "soft": soft,
    }

from datetime import date, datetime
from sqlalchemy.orm import Session

from app.models.history import History


def _model_to_dict(obj) -> dict:
    result = {}
    for c in obj.__table__.columns:
        val = getattr(obj, c.name)
        if isinstance(val, (date, datetime)):
            val = val.isoformat()
        result[c.name] = val
    return result


def record_create(db: Session, entity_type: str, obj, changed_by: str = "system") -> None:
    entry = History(
        entity_type=entity_type,
        entity_id=obj.id,
        action="CREATE",
        changed_by=changed_by,
        before_value=None,
        after_value=_model_to_dict(obj),
    )
    db.add(entry)


def record_update(db: Session, entity_type: str, obj, before: dict, changed_by: str = "system") -> None:
    entry = History(
        entity_type=entity_type,
        entity_id=obj.id,
        action="UPDATE",
        changed_by=changed_by,
        before_value=before,
        after_value=_model_to_dict(obj),
    )
    db.add(entry)


def record_delete(db: Session, entity_type: str, obj, changed_by: str = "system") -> None:
    entry = History(
        entity_type=entity_type,
        entity_id=obj.id,
        action="DELETE",
        changed_by=changed_by,
        before_value=_model_to_dict(obj),
        after_value=None,
    )
    db.add(entry)

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.history import History

router = APIRouter()


class HistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entity_type: str
    entity_id: int
    action: str
    changed_by: Optional[str]
    before_value: Optional[dict]
    after_value: Optional[dict]
    changed_at: Optional[datetime]


@router.get("/", response_model=List[HistoryResponse])
def list_history(
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(History)
    if entity_type:
        q = q.filter(History.entity_type == entity_type)
    if entity_id:
        q = q.filter(History.entity_id == entity_id)
    return q.order_by(History.changed_at.desc()).limit(limit).all()

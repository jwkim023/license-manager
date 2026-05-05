from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSON

from app.database import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)   # "license" / "employee"
    entity_id = Column(Integer, nullable=False, index=True)
    action = Column(String(20), nullable=False)         # CREATE / UPDATE / DELETE
    changed_by = Column(String(200))                   # 변경자
    before_value = Column(JSON)                        # 변경 전 값
    after_value = Column(JSON)                         # 변경 후 값
    changed_at = Column(DateTime, server_default=func.now())

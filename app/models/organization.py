from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    azure_object_id = Column(String(100), unique=True, index=True)  # Azure AD objectId
    display_name = Column(String(200), nullable=False)              # 이름
    email = Column(String(200), unique=True, index=True)            # 이메일
    department = Column(String(100))                                # 부서
    job_title = Column(String(100))                                 # 직책
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    synced_at = Column(DateTime)                                    # Azure 동기화 시각
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    manager = relationship("Employee", remote_side=[id], backref="reports")

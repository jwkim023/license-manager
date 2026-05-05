from sqlalchemy import Column, Integer, String, Date, DateTime, Text, func

from app.database import Base


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)   # 제품명
    account = Column(String(200))                        # 계정
    manager = Column(String(100))                        # 담당자
    department = Column(String(100))                     # 부서
    quantity = Column(Integer, default=1)                # 수량
    expire_date = Column(Date)                           # 만료일
    status = Column(String(20), default="active")        # active / expired / cancelled
    notes = Column(Text)                                 # 비고
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

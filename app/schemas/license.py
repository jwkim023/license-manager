from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LicenseCreate(BaseModel):
    product_name: str
    account: Optional[str] = None
    manager: Optional[str] = None
    department: Optional[str] = None
    quantity: int = 1
    expire_date: Optional[date] = None
    status: str = "active"
    notes: Optional[str] = None


class LicenseUpdate(BaseModel):
    product_name: Optional[str] = None
    account: Optional[str] = None
    manager: Optional[str] = None
    department: Optional[str] = None
    quantity: Optional[int] = None
    expire_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class LicenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    account: Optional[str]
    manager: Optional[str]
    department: Optional[str]
    quantity: int
    expire_date: Optional[date]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

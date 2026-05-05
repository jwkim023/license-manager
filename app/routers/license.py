from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseResponse, LicenseUpdate
from app.services import history as history_svc

router = APIRouter()


@router.get("/", response_model=List[LicenseResponse])
def list_licenses(
    status: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(License)
    if status:
        q = q.filter(License.status == status)
    if department:
        q = q.filter(License.department == department)
    return q.order_by(License.id).all()


@router.get("/{license_id}", response_model=LicenseResponse)
def get_license(license_id: int, db: Session = Depends(get_db)):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")
    return obj


@router.post("/", response_model=LicenseResponse, status_code=201)
def create_license(
    payload: LicenseCreate,
    db: Session = Depends(get_db),
):
    obj = License(**payload.model_dump())
    db.add(obj)
    db.flush()
    history_svc.record_create(db, "license", obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{license_id}", response_model=LicenseResponse)
def update_license(
    license_id: int,
    payload: LicenseUpdate,
    db: Session = Depends(get_db),
):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")

    before = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    db.flush()
    history_svc.record_update(db, "license", obj, before)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{license_id}", status_code=204)
def delete_license(license_id: int, db: Session = Depends(get_db)):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")

    history_svc.record_delete(db, "license", obj)
    db.delete(obj)
    db.commit()

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.license import License
from app.services import history as history_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ── 메인 페이지 ──────────────────────────────────────────────
@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    licenses = db.query(License).order_by(License.id).all()
    return templates.TemplateResponse(request, "index.html", {"licenses": licenses, "today": date.today()})


# ── 테이블 파셜 (HTMX 갱신용) ───────────────────────────────
@router.get("/partials/licenses", response_class=HTMLResponse)
def license_table(request: Request, db: Session = Depends(get_db)):
    licenses = db.query(License).order_by(License.id).all()
    return templates.TemplateResponse(request, "partials/license_table.html", {"licenses": licenses, "today": date.today()})


# ── 폼 모달 파셜 ────────────────────────────────────────────
@router.get("/partials/licenses/form", response_class=HTMLResponse)
def license_form_new(request: Request):
    return templates.TemplateResponse(request, "partials/license_form.html", {"license": None})


@router.get("/partials/licenses/{license_id}/form", response_class=HTMLResponse)
def license_form_edit(license_id: int, request: Request, db: Session = Depends(get_db)):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")
    return templates.TemplateResponse(request, "partials/license_form.html", {"license": obj})


# ── CREATE ──────────────────────────────────────────────────
@router.post("/partials/licenses", response_class=HTMLResponse)
async def create_license_html(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    expire_raw = form.get("expire_date", "").strip()

    obj = License(
        product_name=form.get("product_name", "").strip(),
        account=form.get("account") or None,
        manager=form.get("manager") or None,
        department=form.get("department") or None,
        quantity=int(form.get("quantity") or 1),
        expire_date=date.fromisoformat(expire_raw) if expire_raw else None,
        status=form.get("status", "active"),
        notes=form.get("notes") or None,
    )
    db.add(obj)
    db.flush()
    history_svc.record_create(db, "license", obj)
    db.commit()
    db.refresh(obj)

    licenses = db.query(License).order_by(License.id).all()
    response = templates.TemplateResponse(
        request, "partials/license_table.html", {"licenses": licenses, "today": date.today()}
    )
    response.headers["HX-Trigger"] = "closeModal"
    return response


# ── UPDATE ──────────────────────────────────────────────────
@router.put("/partials/licenses/{license_id}", response_class=HTMLResponse)
async def update_license_html(license_id: int, request: Request, db: Session = Depends(get_db)):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")

    form = await request.form()
    before = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    expire_raw = form.get("expire_date", "").strip()

    obj.product_name = form.get("product_name", "").strip()
    obj.account = form.get("account") or None
    obj.manager = form.get("manager") or None
    obj.department = form.get("department") or None
    obj.quantity = int(form.get("quantity") or 1)
    obj.expire_date = date.fromisoformat(expire_raw) if expire_raw else None
    obj.status = form.get("status", "active")
    obj.notes = form.get("notes") or None

    db.flush()
    history_svc.record_update(db, "license", obj, before)
    db.commit()

    licenses = db.query(License).order_by(License.id).all()
    response = templates.TemplateResponse(
        request, "partials/license_table.html", {"licenses": licenses, "today": date.today()}
    )
    response.headers["HX-Trigger"] = "closeModal"
    return response


# ── DELETE ──────────────────────────────────────────────────
@router.delete("/partials/licenses/{license_id}", response_class=HTMLResponse)
def delete_license_html(license_id: int, request: Request, db: Session = Depends(get_db)):
    obj = db.get(License, license_id)
    if not obj:
        raise HTTPException(status_code=404, detail="License not found")

    history_svc.record_delete(db, "license", obj)
    db.delete(obj)
    db.commit()

    licenses = db.query(License).order_by(License.id).all()
    return templates.TemplateResponse(
        request, "partials/license_table.html", {"licenses": licenses, "today": date.today()}
    )

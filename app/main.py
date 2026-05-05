from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import license, organization, notification, history, pages

app = FastAPI(title="License Manager")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML 페이지 (최우선 등록)
app.include_router(pages.router)

# JSON API
app.include_router(license.router, prefix="/licenses", tags=["licenses"])
app.include_router(organization.router, prefix="/organizations", tags=["organizations"])
app.include_router(notification.router, prefix="/notifications", tags=["notifications"])
app.include_router(history.router, prefix="/history", tags=["history"])

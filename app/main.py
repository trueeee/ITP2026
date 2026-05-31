from __future__ import annotations

import datetime as dt

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session
from .models import Activity, EmissionFactor, User
from .schemas import ActivityOut, UserCreate, UserOut, WeeklyReportOut

app = FastAPI(title="Hållbarhetskollen")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _co2e(category: str, key: str, amount: float, db: Session) -> float | None:
    factor = db.execute(
        select(EmissionFactor).where(
            EmissionFactor.category == category,
            EmissionFactor.key == key,
        )
    ).scalar_one_or_none()
    if factor is None:
        return None
    return round(factor.co2e_per_unit * amount, 4)


# ── API ────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_session)) -> list[User]:
    return list(db.execute(select(User)).scalars().all())


@app.get("/emission-factors")
def list_factors(db: Session = Depends(get_session)):
    return list(db.execute(select(EmissionFactor)).scalars().all())


@app.get("/activities", response_model=list[ActivityOut])
def list_activities(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_session),
):
    stmt = select(Activity)
    if user_id is not None:
        stmt = stmt.where(Activity.user_id == user_id)
    activities = db.execute(stmt).scalars().all()
    out = []
    for a in activities:
        out.append(ActivityOut(
            id=a.id, user_id=a.user_id, category=a.category,
            key=a.key, amount=a.amount, date=a.date,
            co2e=_co2e(a.category, a.key, a.amount, db),
        ))
    return out


@app.get("/reports/weekly", response_model=WeeklyReportOut)
def weekly_report(
    user_id: int = Query(...),
    week_start: dt.date = Query(...),
    db: Session = Depends(get_session),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    end = week_start + dt.timedelta(days=6)
    activities = db.execute(
        select(Activity)
        .where(Activity.user_id == user_id)
        .where(Activity.date >= week_start)
        .where(Activity.date <= end)
    ).scalars().all()
    total = sum(
        c for a in activities
        if (c := _co2e(a.category, a.key, a.amount, db)) is not None
    )
    return WeeklyReportOut(user_id=user_id, week_start=week_start, week_end=end, total_co2e=total)


# ── UI ─────────────────────────────────────────────────────────────────────────

@app.get("/ui", response_class=HTMLResponse)
def ui_home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/ui/users", response_class=HTMLResponse)
def ui_users(request: Request, db: Session = Depends(get_session)):
    users = db.execute(select(User)).scalars().all()
    return templates.TemplateResponse(request, "create_user.html",
        {"request": request, "users": users, "message": None, "error": None})


@app.post("/ui/users", response_class=HTMLResponse)
def ui_create_user(
    request: Request,
    name: str = Form(None),
    db: Session = Depends(get_session),
):
    users_q = lambda: db.execute(select(User)).scalars().all()
    if not name or not name.strip():
        return templates.TemplateResponse(request, "create_user.html",
            {"request": request, "users": users_q(), "message": None, "error": "Namn får inte vara tomt."})
    db.add(User(name=name.strip()))
    db.commit()
    return templates.TemplateResponse(request, "create_user.html",
        {"request": request, "users": users_q(), "message": "Användare skapad!", "error": None})


@app.post("/ui/users/{user_id}/delete", response_class=HTMLResponse)
def ui_delete_user(user_id: int, request: Request, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
    users = db.execute(select(User)).scalars().all()
    return templates.TemplateResponse(request, "create_user.html",
        {"request": request, "users": users, "message": "Användare borttagen.", "error": None})


def _factor_map(db: Session) -> dict:
    factors = db.execute(select(EmissionFactor)).scalars().all()
    result = {}
    for f in factors:
        result.setdefault(f.category, []).append({"key": f.key, "unit": f.unit})
    return result


@app.get("/ui/activities", response_class=HTMLResponse)
def ui_activities(request: Request, filter_user_id: int | None = Query(default=None), db: Session = Depends(get_session)):
    users = db.execute(select(User)).scalars().all()
    stmt = select(Activity)
    if filter_user_id is not None:
        stmt = stmt.where(Activity.user_id == filter_user_id)
    activities = db.execute(stmt).scalars().all()
    rows = [ActivityOut(
        id=a.id, user_id=a.user_id, category=a.category,
        key=a.key, amount=a.amount, date=a.date,
        co2e=_co2e(a.category, a.key, a.amount, db),
    ) for a in activities]
    users_by_id = {u.id: u.name for u in users}
    return templates.TemplateResponse(request, "activities.html",
        {"request": request, "users": users, "activities": rows,
         "factors": _factor_map(db), "selected_user_id": None, "filter_user_id": filter_user_id,
         "users_by_id": users_by_id, "message": None, "error": None})


@app.post("/ui/activities", response_class=HTMLResponse)
def ui_create_activity(
    request: Request,
    user_id: int = Form(...),
    category: str = Form(...),
    key: str = Form(...),
    amount: float = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_session),
):
    users = db.execute(select(User)).scalars().all()

    try:
        parsed_date = dt.date.fromisoformat(date)
    except ValueError:
        return templates.TemplateResponse(request, "activities.html",
            {"request": request, "users": users, "activities": [],
             "factors": _factor_map(db), "selected_user_id": user_id, "message": None, "error": "Ogiltigt datumformat."})

    if amount <= 0:
        return templates.TemplateResponse(request, "activities.html",
            {"request": request, "users": users, "activities": [],
             "factors": _factor_map(db), "selected_user_id": user_id, "message": None, "error": "Mängd måste vara större än 0."})

    user = db.get(User, user_id)
    if not user:
        return templates.TemplateResponse(request, "activities.html",
            {"request": request, "users": users, "activities": [],
             "factors": _factor_map(db), "selected_user_id": None, "message": None, "error": "Användaren finns inte."})

    db.add(Activity(user_id=user_id, category=category, key=key, amount=amount, date=parsed_date))
    db.commit()

    activities = db.execute(select(Activity).where(Activity.user_id == user_id)).scalars().all()
    rows = [ActivityOut(
        id=a.id, user_id=a.user_id, category=a.category,
        key=a.key, amount=a.amount, date=a.date,
        co2e=_co2e(a.category, a.key, a.amount, db),
    ) for a in activities]
    users_by_id = {u.id: u.name for u in users}
    return templates.TemplateResponse(request, "activities.html",
        {"request": request, "users": users, "activities": rows,
         "factors": _factor_map(db), "selected_user_id": user_id, "filter_user_id": user_id,
         "users_by_id": users_by_id, "message": "Aktivitet sparad!", "error": None})


@app.get("/ui/reports/weekly", response_class=HTMLResponse)
def ui_weekly_report(
    request: Request,
    user_id: int | None = None,
    week_start: str | None = None,
    db: Session = Depends(get_session),
):
    users = db.execute(select(User)).scalars().all()
    total = None
    error = None

    if user_id is not None and week_start:
        try:
            start = dt.date.fromisoformat(week_start)
            end = start + dt.timedelta(days=6)
        except ValueError:
            error = "Ogiltigt datumformat, använd YYYY-MM-DD."
        else:
            activities = db.execute(
                select(Activity)
                .where(Activity.user_id == user_id)
                .where(Activity.date >= start)
                .where(Activity.date <= end)
            ).scalars().all()
            total = sum(
                c for a in activities
                if (c := _co2e(a.category, a.key, a.amount, db)) is not None
            )

    return templates.TemplateResponse(request, "weekly.html",
        {"request": request, "users": users, "selected_user_id": user_id,
         "week_start": week_start, "total": total, "error": error})
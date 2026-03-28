from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Tenant
from app.schemas import TenantCreate, TenantOut

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantOut, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Tenant).where((Tenant.slug == payload.slug) | (Tenant.name == payload.name)))
    if existing:
        raise HTTPException(status_code=409, detail="Tenant name or slug already exists")

    tenant = Tenant(name=payload.name.strip(), slug=payload.slug.strip().lower())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

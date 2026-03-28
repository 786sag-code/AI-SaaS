from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models import TicketStatus


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=120)


class TenantOut(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    tenant_slug: str
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: EmailStr
    full_name: str
    is_admin: bool

    model_config = {"from_attributes": True}


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TicketUpdate(BaseModel):
    status: TicketStatus | None = None
    priority: str | None = Field(default=None, pattern="^(low|medium|high)$")
    assignee_id: int | None = None


class TicketOut(BaseModel):
    id: int
    tenant_id: int
    title: str
    description: str
    status: TicketStatus
    priority: str
    ai_suggestion: str | None
    assignee_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}

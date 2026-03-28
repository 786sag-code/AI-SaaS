from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Ticket, User
from app.schemas import TicketCreate, TicketOut, TicketUpdate
from app.tasks import generate_ticket_ai_suggestion

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketOut])
def list_tickets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tickets = db.scalars(
        select(Ticket).where(Ticket.tenant_id == current_user.tenant_id).order_by(Ticket.created_at.desc())
    ).all()
    return tickets


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    payload: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ticket = Ticket(
        tenant_id=current_user.tenant_id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        priority=payload.priority,
        assignee_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # async suggestion generation for non-blocking API request time
    generate_ticket_ai_suggestion.delay(ticket.id)
    return ticket


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id, Ticket.tenant_id == current_user.tenant_id))
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if payload.status is not None:
        ticket.status = payload.status
    if payload.priority is not None:
        ticket.priority = payload.priority
    if payload.assignee_id is not None:
        assignee = db.scalar(
            select(User).where(User.id == payload.assignee_id, User.tenant_id == current_user.tenant_id)
        )
        if not assignee:
            raise HTTPException(status_code=400, detail="Invalid assignee for tenant")
        ticket.assignee_id = payload.assignee_id

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

from celery import Celery
from sqlalchemy import select

from app.core.config import settings
from app.db import SessionLocal
from app.models import Ticket
from app.services.ai import generate_ai_suggestion

celery_app = Celery("support_saas", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


@celery_app.task(name="tickets.generate_ai_suggestion")
def generate_ticket_ai_suggestion(ticket_id: int) -> None:
    db = SessionLocal()
    try:
        ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id))
        if not ticket:
            return
        ticket.ai_suggestion = generate_ai_suggestion(ticket.title, ticket.description)
        db.add(ticket)
        db.commit()
    finally:
        db.close()

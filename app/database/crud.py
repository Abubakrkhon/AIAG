"""CRUD operations for database models"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .models import Customer, Candidate, Interview, InterviewStatus, PaymentPlan


# ============== Customer Operations ==============

def create_customer(
    db: Session,
    company_name: str,
    contact_name: str,
    email: str,
    phone: Optional[str] = None,
    payment_plan: PaymentPlan = PaymentPlan.PAY_PER_HIRE,
    webhook_url: Optional[str] = None,
) -> Customer:
    """Create a new customer"""
    customer = Customer(
        company_name=company_name,
        contact_name=contact_name,
        email=email,
        phone=phone,
        payment_plan=payment_plan,
        webhook_url=webhook_url,
        credits_remaining=0 if payment_plan == PaymentPlan.PAY_PER_HIRE else None,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    """Get customer by ID"""
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    """Get customer by email"""
    return db.query(Customer).filter(Customer.email == email).first()


def update_customer(
    db: Session,
    customer_id: int,
    **updates: Dict[str, Any],
) -> Optional[Customer]:
    """Update customer fields"""
    customer = get_customer(db, customer_id)
    if not customer:
        return None

    for key, value in updates.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


# ============== Candidate Operations ==============

def create_candidate(
    db: Session,
    name: str,
    phone: str,
    job_title: str,
    email: Optional[str] = None,
    source: Optional[str] = None,
) -> Candidate:
    """Create a new candidate"""
    candidate = Candidate(
        name=name,
        phone=phone,
        job_title=job_title,
        email=email,
        source=source,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def get_candidate(db: Session, candidate_id: int) -> Optional[Candidate]:
    """Get candidate by ID"""
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()


def get_candidate_by_phone(db: Session, phone: str) -> Optional[Candidate]:
    """Get candidate by phone number"""
    return db.query(Candidate).filter(Candidate.phone == phone).first()


# ============== Interview Operations ==============

def create_interview(
    db: Session,
    customer_id: int,
    candidate_id: int,
    job_title: str,
    phone_number: str,
    template_name: str = "general",
    custom_questions: Optional[List[str]] = None,
    schedule_link: Optional[str] = None,
) -> Interview:
    """Create a new interview session"""
    interview = Interview(
        customer_id=customer_id,
        candidate_id=candidate_id,
        job_title=job_title,
        phone_number=phone_number,
        template_name=template_name,
        custom_questions=custom_questions or [],
        schedule_link=schedule_link,
        status=InterviewStatus.PENDING,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


def get_interview(db: Session, interview_id: int) -> Optional[Interview]:
    """Get interview by ID"""
    return db.query(Interview).filter(Interview.id == interview_id).first()


def get_interview_by_call_sid(db: Session, call_sid: str) -> Optional[Interview]:
    """Get interview by Twilio call SID"""
    return db.query(Interview).filter(Interview.call_sid == call_sid).first()


def list_interviews(
    db: Session,
    customer_id: Optional[int] = None,
    status: Optional[InterviewStatus] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Interview]:
    """List interviews with optional filters"""
    query = db.query(Interview)

    if customer_id:
        query = query.filter(Interview.customer_id == customer_id)

    if status:
        query = query.filter(Interview.status == status)

    return query.order_by(desc(Interview.created_at)).limit(limit).offset(offset).all()


def update_interview(
    db: Session,
    interview_id: int,
    **updates: Dict[str, Any],
) -> Optional[Interview]:
    """Update interview fields"""
    interview = get_interview(db, interview_id)
    if not interview:
        return None

    for key, value in updates.items():
        if hasattr(interview, key):
            setattr(interview, key, value)

    # Auto-set completed_at if status changed to COMPLETED
    if updates.get("status") == InterviewStatus.COMPLETED and not interview.completed_at:
        interview.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(interview)
    return interview


def complete_interview(
    db: Session,
    interview_id: int,
    score: int,
    qualified: bool,
    transcript: str,
    answers: Dict[str, Any],
    duration_seconds: int,
    notes: Optional[str] = None,
) -> Optional[Interview]:
    """Mark interview as completed with results"""
    return update_interview(
        db,
        interview_id,
        status=InterviewStatus.COMPLETED,
        score=score,
        qualified=qualified,
        transcript=transcript,
        answers=answers,
        duration_seconds=duration_seconds,
        notes=notes,
        completed_at=datetime.utcnow(),
    )


def get_interview_stats(
    db: Session,
    customer_id: int,
    days: int = 30,
) -> Dict[str, Any]:
    """Get interview statistics for a customer using optimized SQL aggregates"""
    from datetime import timedelta
    from sqlalchemy import func, case

    cutoff = datetime.utcnow() - timedelta(days=days)

    # Use database-side aggregates instead of loading all model objects with transcripts/answers into memory
    stats = (
        db.query(
            func.count(Interview.id).label("total"),
            func.count(case((Interview.status == InterviewStatus.COMPLETED, 1))).label("completed"),
            func.count(case((Interview.qualified.is_(True), 1))).label("qualified"),
            func.avg(case((Interview.status == InterviewStatus.COMPLETED, Interview.score))).label("avg_score"),
            func.avg(case((Interview.status == InterviewStatus.COMPLETED, Interview.duration_seconds))).label("avg_duration"),
        )
        .filter(
            Interview.customer_id == customer_id,
            Interview.created_at >= cutoff,
        )
        .one()
    )

    total = stats.total or 0
    completed = stats.completed or 0
    qualified = stats.qualified or 0
    avg_score = float(stats.avg_score or 0.0)
    avg_duration = float(stats.avg_duration or 0.0)

    return {
        "total_interviews": total,
        "completed_interviews": completed,
        "qualified_candidates": qualified,
        "qualification_rate": (qualified / max(1, completed)) * 100,
        "average_score": round(avg_score, 2),
        "average_duration_seconds": round(avg_duration, 2),
        "period_days": days,
    }

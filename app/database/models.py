"""Database models using SQLAlchemy"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

Base = declarative_base()


class PaymentPlan(enum.Enum):
    MONTHLY = "monthly"  # $299/month
    PAY_PER_HIRE = "pay_per_hire"  # $49/hire


class InterviewStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"


class Customer(Base):
    """Business customer (employer)"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    
    # Billing
    payment_plan = Column(SQLEnum(PaymentPlan), default=PaymentPlan.PAY_PER_HIRE)
    stripe_customer_id = Column(String(255), unique=True)
    subscription_status = Column(String(50), default="active")
    credits_remaining = Column(Integer, default=0)  # For pay-per-hire
    
    # Settings
    webhook_url = Column(String(500))  # Zapier/callback URL
    timezone = Column(String(50), default="America/New_York")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interviews = relationship("Interview", back_populates="customer", cascade="all, delete-orphan")


class Candidate(Base):
    """Job candidate being interviewed"""

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(255))
    
    # Interview details
    job_title = Column(String(255), nullable=False)
    source = Column(String(100))  # Indeed, LinkedIn, referral, etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interviews = relationship("Interview", back_populates="candidate")


class Interview(Base):
    """Individual interview session"""

    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    
    # Interview configuration
    job_title = Column(String(255), nullable=False)
    template_name = Column(String(100), default="general")
    custom_questions = Column(JSON, default=list)  # Additional custom questions
    schedule_link = Column(String(500))  # Calendly link for scheduling
    
    # Call details
    call_sid = Column(String(100), unique=True)  # Twilio call SID
    phone_number = Column(String(20), nullable=False)
    
    # Status & results
    status = Column(SQLEnum(InterviewStatus), default=InterviewStatus.PENDING)
    score = Column(Integer)  # 0-100
    qualified = Column(Boolean)
    transcript = Column(Text)  # Full conversation transcript
    answers = Column(JSON)  # Structured Q&A
    notes = Column(Text)
    
    # Timing
    scheduled_time = Column(DateTime)  # When call was scheduled
    started_at = Column(DateTime)  # When call started
    completed_at = Column(DateTime)  # When call ended
    duration_seconds = Column(Integer)
    
    # Cost tracking
    cost_cents = Column(Integer, default=0)  # Track API costs for billing
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="interviews")
    candidate = relationship("Candidate", back_populates="interviews")


# Database setup
engine = None
SessionLocal = None


def init_db(database_url: str = None):
    """Initialize database connection and create tables"""
    global engine, SessionLocal
    
    if database_url is None:
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/interview_ai"
        )
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    return SessionLocal


def get_db():
    """Get database session (for FastAPI dependency injection)"""
    if SessionLocal is None:
        init_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

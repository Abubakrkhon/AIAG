"""Tests for database CRUD operations"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Customer, Candidate, Interview, InterviewStatus, PaymentPlan
from app.database import crud


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database session for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_customer_crud(db_session):
    customer = crud.create_customer(
        db=db_session,
        company_name="Acme Corp",
        contact_name="Alice",
        email="alice@acme.com",
    )
    assert customer.id is not None
    assert customer.company_name == "Acme Corp"

    fetched = crud.get_customer(db_session, customer.id)
    assert fetched.email == "alice@acme.com"

    fetched_by_email = crud.get_customer_by_email(db_session, "alice@acme.com")
    assert fetched_by_email.id == customer.id

    updated = crud.update_customer(db_session, customer.id, company_name="Acme Inc")
    assert updated.company_name == "Acme Inc"


def test_candidate_crud(db_session):
    candidate = crud.create_candidate(
        db=db_session,
        name="Bob Smith",
        phone="+15550001111",
        job_title="Technician",
    )
    assert candidate.id is not None
    assert candidate.name == "Bob Smith"

    fetched = crud.get_candidate_by_phone(db_session, "+15550001111")
    assert fetched.id == candidate.id


def test_interview_stats(db_session):
    customer = crud.create_customer(
        db=db_session,
        company_name="Test Company",
        contact_name="Bob",
        email="bob@test.com",
    )
    candidate1 = crud.create_candidate(
        db=db_session, name="Cand 1", phone="+111", job_title="Dev"
    )
    candidate2 = crud.create_candidate(
        db=db_session, name="Cand 2", phone="+222", job_title="Dev"
    )

    # Completed & Qualified interview
    i1 = crud.create_interview(
        db=db_session,
        customer_id=customer.id,
        candidate_id=candidate1.id,
        job_title="Dev",
        phone_number="+111",
    )
    crud.complete_interview(
        db=db_session,
        interview_id=i1.id,
        score=80,
        qualified=True,
        transcript="Interview text 1",
        answers={"q1": "a1"},
        duration_seconds=300,
    )

    # Completed & Not Qualified interview
    i2 = crud.create_interview(
        db=db_session,
        customer_id=customer.id,
        candidate_id=candidate2.id,
        job_title="Dev",
        phone_number="+222",
    )
    crud.complete_interview(
        db=db_session,
        interview_id=i2.id,
        score=50,
        qualified=False,
        transcript="Interview text 2",
        answers={"q1": "a2"},
        duration_seconds=180,
    )

    # Pending interview
    crud.create_interview(
        db=db_session,
        customer_id=customer.id,
        candidate_id=candidate2.id,
        job_title="Dev",
        phone_number="+222",
    )

    stats = crud.get_interview_stats(db_session, customer.id, days=30)
    assert stats["total_interviews"] == 3
    assert stats["completed_interviews"] == 2
    assert stats["qualified_candidates"] == 1
    assert stats["qualification_rate"] == 50.0
    assert stats["average_score"] == 65.0
    assert stats["average_duration_seconds"] == 240.0

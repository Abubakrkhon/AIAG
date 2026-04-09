"""Zapier webhook integration for no-code setup"""

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import os

from app.database.models import get_db
from app.database import crud
from app.twilio.outbound import make_outbound_call

router = APIRouter()


@router.post("/zapier")
async def handle_zapier_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Zapier webhook endpoint for triggering interviews.
    
    This allows any Zapier user to connect Interview.ai without API knowledge.
    
    Expected Zapier payload:
    {
        "candidate_name": "John Doe",
        "candidate_phone": "+15551234567",
        "candidate_email": "john@example.com",
        "job_title": "HVAC Technician",
        "template": "skilled_trades",  # optional, defaults to "general"
        "custom_questions": ["Question 1?", "Question 2?"],  # optional
        "schedule_link": "https://calendly.com/...",  # optional
        "callback_url": "https://yourcompany.com/webhook"  # optional
    }
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Validate required fields
    required_fields = ["candidate_name", "candidate_phone", "job_title"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}",
            )

    # Get or create customer (use email as identifier)
    customer_email = data.get("customer_email", "zapier-integration@interview.ai")
    customer = crud.get_customer_by_email(db, customer_email)
    
    if not customer:
        # Create new customer for this Zapier integration
        customer = crud.create_customer(
            db=db,
            company_name=data.get("company_name", "Zapier Integration"),
            contact_name=data.get("contact_name", "Zapier User"),
            email=customer_email,
            phone=data.get("company_phone"),
            webhook_url=data.get("callback_url"),
        )

    # Get or create candidate
    candidate = crud.get_candidate_by_phone(db, data["candidate_phone"])
    
    if not candidate:
        candidate = crud.create_candidate(
            db=db,
            name=data["candidate_name"],
            phone=data["candidate_phone"],
            job_title=data["job_title"],
            email=data.get("candidate_email"),
            source=data.get("source", "zapier"),
        )

    # Create interview record
    interview = crud.create_interview(
        db=db,
        customer_id=customer.id,
        candidate_id=candidate.id,
        job_title=data["job_title"],
        phone_number=data["candidate_phone"],
        template_name=data.get("template", "general"),
        custom_questions=data.get("custom_questions", []),
        schedule_link=data.get("schedule_link"),
    )

    # Trigger outbound call immediately
    call_result = await make_outbound_call(
        to_number=data["candidate_phone"],
        candidate_name=data["candidate_name"],
        job_title=data["job_title"],
        template=data.get("template", "general"),
    )

    if call_result.get("success"):
        # Update interview with call SID
        crud.update_interview(
            db=db,
            interview_id=interview.id,
            call_sid=call_result["call_sid"],
            status="in_progress",
        )

        return {
            "success": True,
            "interview_id": interview.id,
            "call_sid": call_result["call_sid"],
            "status": "initiated",
            "message": f"Interview call initiated for {data['candidate_name']}",
        }
    else:
        # Call failed, but interview record exists
        crud.update_interview(
            db=db,
            interview_id=interview.id,
            status="failed",
            notes=f"Call initiation failed: {call_result.get('error')}",
        )

        return {
            "success": False,
            "interview_id": interview.id,
            "error": call_result.get("error"),
            "message": "Interview record created but call failed",
        }


@router.post("/zapier/schedule")
async def schedule_via_zapier(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Schedule an interview for a future time via Zapier.
    
    Payload:
    {
        "candidate_name": "John Doe",
        "candidate_phone": "+15551234567",
        "job_title": "Position",
        "scheduled_time": "2024-01-15T14:00:00Z",
        ... (same fields as /zapier)
    }
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Similar to /zapier but schedules for later
    # Would use Celery beat or similar to trigger at scheduled_time
    
    return {
        "success": True,
        "scheduled": True,
        "scheduled_time": data.get("scheduled_time"),
        "message": "Interview scheduled (implementation pending)",
    }


@router.get("/zapier/test")
async def test_zapier_connection():
    """Test endpoint for Zapier connection verification"""
    return {
        "status": "connected",
        "service": "Interview.ai",
        "version": "1.0.0",
        "endpoints": {
            "trigger_interview": "/webhook/zapier",
            "schedule_interview": "/webhook/zapier/schedule",
        },
    }


@router.get("/zapier/actions")
async def list_zapier_actions():
    """
    List available actions for Zapier integration.
    
    This helps Zapier auto-configure the integration.
    """
    return {
        "actions": [
            {
                "key": "trigger_interview",
                "name": "Trigger Interview Call",
                "description": "Immediately call a candidate and conduct automated screening interview",
                "required_fields": ["candidate_name", "candidate_phone", "job_title"],
                "optional_fields": [
                    "candidate_email",
                    "template",
                    "custom_questions",
                    "schedule_link",
                    "callback_url",
                ],
            },
            {
                "key": "schedule_interview",
                "name": "Schedule Interview Call",
                "description": "Schedule an automated interview call for a future time",
                "required_fields": [
                    "candidate_name",
                    "candidate_phone",
                    "job_title",
                    "scheduled_time",
                ],
            },
            {
                "key": "get_interview_status",
                "name": "Get Interview Status",
                "description": "Check the status and results of a completed interview",
                "required_fields": ["interview_id"],
            },
        ]
    }

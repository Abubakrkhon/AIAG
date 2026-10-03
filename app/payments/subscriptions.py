"""Stripe payment integration for subscriptions and pay-per-hire"""

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import stripe
import os

from app.database.models import get_db, Customer, PaymentPlan
from app.database import crud

router = APIRouter()

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Price IDs (configured in Stripe Dashboard)
PRICE_ID_MONTHLY = os.getenv("STRIPE_PRICE_ID_MONTHLY", "price_monthly_299")
PRICE_ID_PER_HIRE = os.getenv("STRIPE_PRICE_ID_PER_HIRE", "price_per_hire_49")


@router.post("/checkout-session")
async def create_checkout_session(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Create a Stripe Checkout session for subscription or credits.

    Payload:
    {
        "customer_email": "business@example.com",
        "plan": "monthly" | "pay_per_hire",
        "credits": 10,  # optional, for pay-per-hire bundles
    }
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    customer_email = data.get("customer_email")
    plan = data.get("plan", "pay_per_hire")

    if not customer_email:
        raise HTTPException(status_code=400, detail="customer_email required")

    # Determine price ID and mode
    if plan == "monthly":
        price_id = PRICE_ID_MONTHLY
        mode = "subscription"
    else:
        # Pay-per-hire: sell credit bundles
        credits = data.get("credits", 10)
        # Could use different price IDs for different bundle sizes
        price_id = PRICE_ID_PER_HIRE
        mode = "payment"

    # Get or create Stripe customer
    existing_customer = crud.get_customer_by_email(db, customer_email)
    stripe_customer_id = None

    if existing_customer and existing_customer.stripe_customer_id:
        stripe_customer_id = existing_customer.stripe_customer_id

    # Create checkout session
    success_url = str(request.base_url) + "payment/success?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = str(request.base_url) + "payment/cancel"

    session = stripe.checkout.Session.create(
        customer=stripe_customer_id,
        customer_email=customer_email if not stripe_customer_id else None,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode=mode,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "plan": plan,
            "credits": str(credits) if plan != "monthly" else "0",
            "customer_email": customer_email,
        },
    )

    return {
        "session_id": session.id,
        "url": session.url,
        "plan": plan,
        "amount_total": session.amount_total,
    }


@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    Handle Stripe webhook events.

    Events handled:
    - checkout.session.completed: Activate subscription or add credits
    - customer.subscription.updated: Update subscription status
    - customer.subscription.deleted: Cancel subscription
    - invoice.payment_failed: Notify customer
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not webhook_secret or not sig_header:
        # In development, allow without signature verification
        event = request.json() if hasattr(request, "json") else await request.json()
    else:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        await _handle_checkout_completed(data_object)

    elif event_type == "customer.subscription.updated":
        await _handle_subscription_updated(data_object)

    elif event_type == "customer.subscription.deleted":
        await _handle_subscription_deleted(data_object)

    elif event_type == "invoice.payment_failed":
        await _handle_payment_failed(data_object)

    return {"status": "ok"}


async def _handle_checkout_completed(session_data: Dict[str, Any]):
    """Handle successful checkout completion"""
    from app.database.models import init_db

    db = next(get_db())
    try:
        customer_email = session_data.get("customer_email")
        metadata = session_data.get("metadata", {})
        plan = metadata.get("plan", "pay_per_hire")

        if not customer_email:
            return

        # Get or create customer
        customer = crud.get_customer_by_email(db, customer_email)

        if not customer:
            customer = crud.create_customer(
                db=db,
                company_name=metadata.get("company_name", "New Customer"),
                contact_name=metadata.get("contact_name", customer_email.split("@")[0]),
                email=customer_email,
            )

        # Update Stripe customer ID
        if session_data.get("customer"):
            crud.update_customer(
                db=db,
                customer_id=customer.id,
                stripe_customer_id=session_data["customer"],
            )

        # Activate based on plan type
        if plan == "monthly":
            crud.update_customer(
                db=db,
                customer_id=customer.id,
                payment_plan=PaymentPlan.MONTHLY,
                subscription_status="active",
            )
        else:
            # Add credits for pay-per-hire
            credits = int(metadata.get("credits", 10))
            current_credits = customer.credits_remaining or 0
            crud.update_customer(
                db=db,
                customer_id=customer.id,
                payment_plan=PaymentPlan.PAY_PER_HIRE,
                credits_remaining=current_credits + credits,
            )

            # Charge for one interview immediately (or track credits)
            # This is simplified - in production, deduct credits per interview

    finally:
        db.close()


async def _handle_subscription_updated(subscription_data: Dict[str, Any]):
    """Handle subscription status updates"""
    db = next(get_db())
    try:
        customer_email = subscription_data.get("customer_email")
        status = subscription_data.get("status")

        if customer_email:
            customer = crud.get_customer_by_email(db, customer_email)
            if customer:
                crud.update_customer(
                    db=db,
                    customer_id=customer.id,
                    subscription_status=status,
                )
    finally:
        db.close()


async def _handle_subscription_deleted(subscription_data: Dict[str, Any]):
    """Handle subscription cancellation"""
    db = next(get_db())
    try:
        customer_id = subscription_data.get("customer")
        # Find customer by Stripe ID and update status
        # Implementation depends on how you store Stripe customer IDs
    finally:
        db.close()


async def _handle_payment_failed(invoice_data: Dict[str, Any]):
    """Handle failed payment notification"""
    # Send email notification to customer
    # Could downgrade to pay-per-hire after X failed attempts
    pass


@router.get("/pricing")
async def get_pricing_plans():
    """Return available pricing plans"""
    return {
        "plans": [
            {
                "name": "Pay Per Hire",
                "id": "pay_per_hire",
                "price": 49,
                "currency": "USD",
                "billing": "per_interview",
                "description": "$49 per successful interview scheduled",
                "best_for": "Low-volume hiring (5-10/year)",
                "features": [
                    "No monthly commitment",
                    "Pay only for qualified candidates",
                    "Standard templates",
                    "Email support",
                ],
            },
            {
                "name": "Monthly Unlimited",
                "id": "monthly",
                "price": 299,
                "currency": "USD",
                "billing": "monthly",
                "description": "$299/month for up to 20 interviews",
                "overage_price": 35,
                "best_for": "High-volume hiring (20+/year)",
                "features": [
                    "Up to 20 interviews/month",
                    "$35 per overage interview",
                    "Custom question templates",
                    "Priority support",
                    "Advanced analytics",
                    "Zapier integration",
                ],
            },
            {
                "name": "Staffing Agency",
                "id": "agency",
                "price": "custom",
                "currency": "USD",
                "billing": "custom",
                "description": "Custom pricing for staffing agencies",
                "best_for": "Staffing agencies & recruiters",
                "features": [
                    "Unlimited interviews",
                    "White-label option",
                    "API access",
                    "Dedicated support",
                    "Custom integrations",
                    "Volume discounts",
                ],
                "contact": "sales@interview.ai",
            },
        ]
    }

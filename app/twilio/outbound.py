"""Outbound calling functionality using Twilio"""

from typing import Optional, Dict, Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from datetime import datetime, timedelta


class OutboundCallService:
    """Manage outbound interview calls"""

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
        webhook_base_url: str,
    ):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
        self.webhook_base_url = webhook_base_url

    async def make_interview_call(
        self,
        to_number: str,
        candidate_name: str,
        job_title: str,
        template: str = "general",
        callback_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Place an outbound interview call.
        
        Args:
            to_number: Candidate's phone number
            candidate_name: Candidate's name
            job_title: Position they applied for
            template: Interview template to use
            callback_url: URL to send results
            
        Returns:
            Call details including SID and status
        """
        try:
            # Build TwiML URL with parameters
            twiml_url = f"{self.webhook_base_url}/twilio/voice/interview"
            
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                url=twiml_url,
                status_callback=f"{self.webhook_base_url}/twilio/call-status",
                status_callback_event=["initiated", "ringing", "answered", "completed"],
            )

            result = {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "to": to_number,
                "from": self.from_number,
                "candidate_name": candidate_name,
                "job_title": job_title,
                "initiated_at": datetime.now().isoformat(),
            }

            return result

        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": e.code,
                "to": to_number,
                "candidate_name": candidate_name,
            }

    def schedule_call(
        self,
        to_number: str,
        candidate_name: str,
        job_title: str,
        scheduled_time: datetime,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Schedule a call for a future time.
        
        In production, this would use Celery beat or similar
        to trigger the call at the scheduled time.
        """
        # For now, just validate and return scheduling info
        if scheduled_time <= datetime.now():
            return {
                "success": False,
                "error": "Scheduled time must be in the future",
            }

        return {
            "success": True,
            "scheduled": True,
            "scheduled_time": scheduled_time.isoformat(),
            "to_number": to_number,
            "candidate_name": candidate_name,
            "job_title": job_title,
            "message": f"Call scheduled for {scheduled_time}",
        }

    def cancel_call(self, call_sid: str) -> Dict[str, Any]:
        """Cancel an in-progress or scheduled call"""
        try:
            # Can only cancel calls that haven't been answered
            call = self.client.calls(call_sid).update(status="canceled")
            return {
                "success": True,
                "call_sid": call_sid,
                "status": call.status,
            }
        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e),
                "call_sid": call_sid,
            }

    def get_call_status(self, call_sid: str) -> Dict[str, Any]:
        """Get current status of a call"""
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "duration": call.duration,
                "start_time": str(call.start_time) if call.start_time else None,
                "end_time": str(call.end_time) if call.end_time else None,
                "to": call.to,
                "from": call.from_,
            }
        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e),
                "call_sid": call_sid,
            }


# Singleton instance (initialized in app startup)
_call_service: Optional[OutboundCallService] = None


def get_call_service() -> OutboundCallService:
    """Get or create the outbound call service"""
    global _call_service
    
    if _call_service is None:
        _call_service = OutboundCallService(
            account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
            auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
            from_number=os.getenv("TWILIO_PHONE_NUMBER"),
            webhook_base_url=os.getenv("TWILIO_WEBHOOK_BASE_URL", "http://localhost:8000"),
        )
    
    return _call_service


async def make_outbound_call(
    to_number: str,
    candidate_name: str,
    job_title: str,
    **kwargs,
) -> Dict[str, Any]:
    """Convenience function to make an outbound call"""
    service = get_call_service()
    return await service.make_interview_call(
        to_number=to_number,
        candidate_name=candidate_name,
        job_title=job_title,
        **kwargs,
    )


async def schedule_interview_call(
    to_number: str,
    candidate_name: str,
    job_title: str,
    scheduled_time: datetime,
    **kwargs,
) -> Dict[str, Any]:
    """Convenience function to schedule a call"""
    service = get_call_service()
    return service.schedule_call(
        to_number=to_number,
        candidate_name=candidate_name,
        job_title=job_title,
        scheduled_time=scheduled_time,
        **kwargs,
    )

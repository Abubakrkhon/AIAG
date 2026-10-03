"""Twilio webhook handlers for incoming/outgoing calls"""

from fastapi import APIRouter, Request, Form, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from typing import Optional
import os

router = APIRouter()


@router.post("/voice")
async def handle_incoming_call(
    From: str = Form(...),
    To: str = Form(...),
    CallSid: str = Form(...),
    Direction: str = Form("inbound"),
):
    """
    Handle incoming calls to the Interview.ai number.

    For inbound calls (e.g., candidates calling back),
    provide status or route to human operator.
    """
    response = VoiceResponse()

    if Direction == "inbound":
        # Candidate calling back - check interview status
        response.say(
            "Thank you for calling Interview.ai. "
            "If you're a candidate checking on your application status, "
            "please visit our website or wait for the employer to contact you. "
            "For support, press 1.",
            voice="alice",
        )

        with response.gather(num_digits=1, action="/voice/support") as g:
            pass  # If no input, repeat message

    return Response(str(response), media_type="application/xml")


@router.post("/voice/interview")
async def handle_interview_call(
    CallSid: str = Form(...),
    candidate_name: Optional[str] = None,
    job_title: Optional[str] = None,
):
    """
    Start an automated interview call.

    This is triggered when an outbound call is answered.
    Begins the interview flow using the configured template.
    """
    response = VoiceResponse()

    # Introduction
    intro_text = (
        f"Hi {candidate_name or 'there'}, this is an automated screening call "
        f"for the {job_title or 'position'} position. "
        "This call will be recorded and should take about 5 minutes. "
        "Let's get started!"
    )

    response.say(intro_text, voice="alice")

    # First question with gather for response
    # In production, this would use <Record> or streaming
    response.say(
        "Can you tell me about your previous work experience?",
        voice="alice",
    )

    # Record response (max 60 seconds)
    response.record(
        max_length=60,
        action="/voice/process-response",
        timeout=5,
        transcribe=True,
        transcribe_callback="/voice/transcription-complete",
    )

    return Response(str(response), media_type="application/xml")


@router.post("/voice/process-response")
async def process_response(
    RecordingUrl: str = Form(...),
    RecordingDuration: str = Form(...),
    CallSid: str = Form(...),
):
    """
    Process recorded response from candidate.

    In production, this would:
    1. Send recording to Deepgram for transcription
    2. Use GPT-4 to evaluate response
    3. Continue to next question
    """
    response = VoiceResponse()

    # Acknowledge and move to next question
    response.say("Thank you. Next question:", voice="alice")
    response.say(
        "What is your availability? Are you available weekends or evenings?",
        voice="alice",
    )

    response.record(
        max_length=60,
        action="/voice/process-response",  # Loop back for next question
        timeout=5,
        transcribe=True,
    )

    return Response(str(response), media_type="application/xml")


@router.post("/voice/support")
async def handle_support_menu(Digits: str = Form(None)):
    """Handle support menu options"""
    response = VoiceResponse()

    if Digits == "1":
        response.say(
            "For technical support, please email support@interview-ai.com. "
            "We typically respond within 2 hours during business days.",
            voice="alice",
        )
    else:
        response.say("Invalid option. Goodbye.", voice="alice")

    response.hangup()
    return Response(str(response), media_type="application/xml")


@router.post("/voice/transcription-complete")
async def transcription_complete(
    CallSid: str = Form(...),
    TranscriptionStatus: str = Form(...),
    TranscriptionText: str = Form(None),
):
    """
    Callback when Twilio completes transcription.

    Store transcription and continue interview flow.
    """
    response = VoiceResponse()

    if TranscriptionStatus == "completed" and TranscriptionText:
        # Log transcription (would save to DB in production)
        print(f"Transcription for {CallSid}: {TranscriptionText}")

        # Continue to next question or wrap up
        response.say("Great, thank you. One more question:", voice="alice")
        response.say(
            "When would you be able to start if offered this position?",
            voice="alice",
        )

        response.record(
            max_length=60,
            action="/voice/finalize-interview",
            timeout=5,
            transcribe=True,
        )
    else:
        response.say("I didn't catch that. Let's move on.", voice="alice")

    return Response(str(response), media_type="application/xml")


@router.post("/voice/finalize-interview")
async def finalize_interview(CallSid: str = Form(...)):
    """Wrap up the interview call"""
    response = VoiceResponse()

    response.say(
        "Thank you for completing this screening interview. "
        "The hiring team will review your responses and contact you "
        "within 2 business days. Have a great day!",
        voice="alice",
    )
    response.hangup()

    # In production: trigger final scoring, send summary to employer

    return Response(str(response), media_type="application/xml")


@router.post("/sms")
async def handle_sms(
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(...),
):
    """Handle incoming SMS messages"""
    response = MessagingResponse()

    # Auto-reply to candidate inquiries
    response.message(
        "Thanks for your message! For interview scheduling, "
        "please check your email or visit our candidate portal."
    )

    return Response(str(response), media_type="application/xml")

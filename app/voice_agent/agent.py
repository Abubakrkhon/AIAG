"""Voice AI Agent for conducting phone interviews"""

import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime
from pydantic import BaseModel
import openai
try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        ElevenLabs = None
try:
    from deepgram import DeepgramClient, PrerecordedOptions, Source
except ImportError:
    from deepgram import DeepgramClient, PrerecordedOptions
    Source = None

from .prompts import InterviewTemplate, get_template


class InterviewResult(BaseModel):
    candidate_name: str
    candidate_phone: str
    job_title: str
    template_used: str
    answers: Dict[str, Any]
    score: int
    qualified: bool
    transcript: str
    duration_seconds: int
    scheduled_time: Optional[str] = None
    notes: str = ""


class VoiceAgent:
    """
    Voice AI agent that conducts automated phone interviews.

    Flow:
    1. Call candidate via Twilio
    2. Introduce purpose of call
    3. Ask templated questions (5-7 questions)
    4. Transcribe responses using Deepgram
    5. Score responses using GPT-4
    6. Schedule qualified candidates
    7. Send summary to employer
    """

    def __init__(
        self,
        openai_api_key: str,
        elevenlabs_api_key: Optional[str] = None,
        deepgram_api_key: Optional[str] = None,
    ):
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        self.elevenlabs_client = (
            ElevenLabs(api_key=elevenlabs_api_key) if elevenlabs_api_key else None
        )
        self.deepgram_client = (
            DeepgramClient(deepgram_api_key) if deepgram_api_key else None
        )
        self.voice_id = "Rachel"  # Default natural female voice

    async def conduct_interview(
        self,
        candidate_name: str,
        candidate_phone: str,
        job_title: str,
        template_name: str,
        custom_questions: Optional[List[str]] = None,
        schedule_link: Optional[str] = None,
    ) -> InterviewResult:
        """
        Conduct a full phone interview with a candidate.

        Args:
            candidate_name: Name of the candidate
            candidate_phone: Phone number to call
            job_title: Job title they're applying for
            template_name: Template to use (e.g., "general", "trades", "healthcare")
            custom_questions: Optional custom questions to add
            schedule_link: Calendly or similar link for scheduling

        Returns:
            InterviewResult with answers, score, and qualification status
        """
        # Get template
        template = get_template(template_name)

        # Add custom questions if provided
        if custom_questions:
            from .prompts import Question
            for q_text in custom_questions:
                template.questions.append(
                    Question(text=q_text, type="open", required=False)
                )

        # Initialize interview session
        transcript_parts = []
        answers = {}
        start_time = datetime.now()

        # Opening statement
        intro = f"""Hi {candidate_name}, this is an automated screening call from the hiring team for the {job_title} position.
        This call will take about {template.duration_minutes} minutes. Your responses will be recorded and reviewed by the hiring team.
        Let's get started!"""

        transcript_parts.append(f"AI: {intro}")

        # Ask each question
        for idx, question in enumerate(template.questions):
            # Convert question to speech
            question_audio = await self._text_to_speech(question.text)

            # In production, this would play audio via Twilio and capture response
            # For now, we'll simulate the flow
            response_text = await self._simulate_candidate_response(question)

            transcript_parts.append(f"AI: {question.text}")
            transcript_parts.append(f"Candidate: {response_text}")

            # Store answer
            answers[question.text] = response_text

        # Closing and scheduling
        if schedule_link:
            closing = f"""Thank you for your time, {candidate_name}. Based on your responses,
            we'd like to invite you to schedule an in-person interview.
            Please visit {schedule_link} to choose a convenient time."""
        else:
            closing = f"""Thank you for your time, {candidate_name}.
            The hiring team will review your responses and contact you within 2 business days."""

        transcript_parts.append(f"AI: {closing}")

        # Calculate score
        score = await self._score_interview(answers, template)
        qualified = score >= template.passing_score

        # Compile results
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds())

        result = InterviewResult(
            candidate_name=candidate_name,
            candidate_phone=candidate_phone,
            job_title=job_title,
            template_used=template_name,
            answers=answers,
            score=score,
            qualified=qualified,
            transcript="\n".join(transcript_parts),
            duration_seconds=duration,
            notes=f"Score: {score}/100, Qualified: {'Yes' if qualified else 'No'}",
        )

        return result

    async def _text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using ElevenLabs or OpenAI TTS"""
        if self.elevenlabs_client:
            audio = self.elevenlabs_client.generate(
                text=text,
                voice=self.voice_id,
                model="eleven_monolingual_v1",
            )
            return audio

        # Fallback to OpenAI TTS
        response = await self.openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        return response.content

    async def _transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe candidate response using Deepgram"""
        if not self.deepgram_client:
            # Fallback to Whisper
            pass

        # Use Deepgram for phone audio (optimized for phone calls)
        payload = {"buffer": audio_data}
        options = PrerecordedOptions(
            model="nova-2-phonecall",
            smart_format=True,
            utterances=True,
        )

        response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
            payload, options
        )
        return response.results.channels[0].alternatives[0].transcript

    async def _simulate_candidate_response(self, question) -> str:
        """
        Simulate candidate response for testing.
        In production, this captures actual audio from Twilio stream.
        """
        # Use GPT to generate realistic response
        prompt = f"""You are a job candidate being asked an interview question.
        Provide a realistic, concise spoken response (2-3 sentences max).

        Question: {question.text}
        Type: {question.type}
        """

        if question.options:
            prompt += f"\nOptions: {', '.join(question.options)}"

        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a job candidate giving natural spoken responses."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
        )

        return response.choices[0].message.content

    async def _score_interview(
        self, answers: Dict[str, Any], template: InterviewTemplate
    ) -> int:
        """
        Score interview responses using GPT-4.
        Returns score 0-100.
        """
        scoring_prompt = f"""You are an expert hiring manager evaluating interview responses.

        Job Role: Based on {template.name} template
        Industry: {template.industry}

        Evaluate these responses and provide a score from 0-100.
        Consider: clarity, relevance, experience level, enthusiasm, and fit.

        Responses:
        {chr(10).join(f"- Q: {q}\\n  A: {a}" for q, a in answers.items())}

        Provide ONLY a numeric score (0-100), nothing else."""

        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an objective hiring evaluator."},
                {"role": "user", "content": scoring_prompt},
            ],
            max_tokens=10,
        )

        try:
            score = int(response.choices[0].message.content.strip())
            return max(0, min(100, score))  # Clamp to 0-100
        except ValueError:
            return 65  # Default passing score

    def generate_summary_report(self, result: InterviewResult) -> str:
        """Generate a human-readable summary for the employer"""
        status = "✅ QUALIFIED" if result.qualified else "❌ NOT QUALIFIED"

        report = f"""
# Interview Summary Report

**Candidate:** {result.candidate_name}
**Phone:** {result.candidate_phone}
**Position:** {result.job_title}
**Status:** {status}
**Score:** {result.score}/100
**Duration:** {result.duration_seconds} seconds

## Key Answers:
"""
        for question, answer in result.answers.items():
            report += f"\n**Q:** {question}\n**A:** {answer}\n"

        if result.scheduled_time:
            report += f"\n## Scheduled Interview: {result.scheduled_time}"

        report += f"\n\n---\nFull transcript available in dashboard."

        return report

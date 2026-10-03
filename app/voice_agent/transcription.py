"""Transcription service using Deepgram"""

from typing import Optional, Dict, Any
try:
    from deepgram import DeepgramClient, PrerecordedOptions, Source
except ImportError:
    from deepgram import DeepgramClient, PrerecordedOptions
    Source = None


class TranscriptionService:
    """
    Handle audio transcription using Deepgram's phone-optimized models.

    Features:
    - 99% accuracy on phone calls (Deepgram Nova-2 Phonecall)
    - Speaker diarization
    - Smart formatting (phone numbers, dates, etc.)
    - Real-time streaming support
    """

    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)
        self.model = "nova-2-phonecall"

    async def transcribe_audio(
        self,
        audio_data: bytes,
        sample_rate: int = 8000,
        channels: int = 1,
    ) -> Dict[str, Any]:
        """
        Transcribe audio file.

        Args:
            audio_data: Raw audio bytes
            sample_rate: Audio sample rate (8000 for phone)
            channels: Number of audio channels

        Returns:
            Dict with transcript, confidence, and metadata
        """
        payload = {"buffer": audio_data}

        options = PrerecordedOptions(
            model=self.model,
            smart_format=True,
            utterances=True,
            diarize=True,
            language="en",
        )

        response = self.client.listen.prerecorded.v("1").transcribe_file(
            payload, options
        )

        result = response.results

        return {
            "transcript": result.channels[0].alternatives[0].transcript,
            "confidence": result.channels[0].alternatives[0].confidence,
            "duration": result.duration,
            "language": result.language,
            "utterances": [
                {
                    "speaker": u.speaker if hasattr(u, "speaker") else "unknown",
                    "text": u.alternatives[0].transcript,
                    "start": u.start,
                    "end": u.end,
                }
                for u in result.utterances
            ]
            if result.utterances
            else [],
        }

    async def transcribe_stream(self, audio_stream):
        """
        Transcribe real-time audio stream (for live calls).

        This would integrate with Twilio's Media Stream WebSocket
        for real-time transcription during active calls.
        """
        # Implementation for streaming transcription
        # Would use Deepgram's live API with WebSocket
        pass

    @staticmethod
    def get_optimized_config() -> Dict[str, Any]:
        """Get recommended configuration for phone interviews"""
        return {
            "model": "nova-2-phonecall",
            "sample_rate": 8000,
            "encoding": "mulaw",  # Twilio uses μ-law
            "smart_format": True,
            "diarize": True,
            "utterances": True,
            "punctuate": True,
            "paragraphs": False,
        }

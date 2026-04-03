"""
Audio Parser using Whisper
"""
import whisper
from typing import Dict, List
from pathlib import Path


class AudioParser:
    def __init__(self, model_name: str = "base"):
        self.supported_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        self.model = whisper.load_model(model_name)
    
    def parse(self, audio_path: str, language: str = "ru") -> Dict[str, any]:
        """
        Transcribe audio file using Whisper
        
        Returns:
            Dict with:
            - text: full transcription
            - segments: list of timed segments
            - metadata: audio info
        """
        audio_file = Path(audio_path)
        
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Transcribe with Whisper
        result = self.model.transcribe(
            str(audio_file),
            language=language,
            task="transcribe"
        )
        
        segments = []
        for segment in result['segments']:
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return {
            'text': result['text'].strip(),
            'segments': segments,
            'metadata': {
                'source': str(audio_file),
                'duration': result.get('duration', 0),
                'language': result.get('language', language),
                'type': 'audio'
            },
            'source': str(audio_file),
            'type': 'audio'
        }
    
    def parse_with_topics(self, audio_path: str, llm_client=None) -> Dict[str, any]:
        """
        Transcribe and split by topics using LLM
        """
        # First get basic transcription
        result = self.parse(audio_path)
        
        # If LLM client provided, analyze topics
        if llm_client:
            topics = self._detect_topics_segments(result['segments'], llm_client)
            result['topic_segments'] = topics
        
        return result
    
    def _detect_topic_segments(self, segments: List[Dict], llm_client) -> List[Dict]:
        """Use LLM to detect topic boundaries in segments"""
        # Group segments into larger chunks for analysis
        chunk_size = 10
        chunks = []
        
        for i in range(0, len(segments), chunk_size):
            chunk_text = ' '.join([s['text'] for s in segments[i:i+chunk_size]])
            chunks.append({
                'start_idx': i,
                'end_idx': min(i + chunk_size, len(segments)),
                'text': chunk_text,
                'start_time': segments[i]['start'] if i < len(segments) else 0,
                'end_time': segments[min(i + chunk_size - 1, len(segments) - 1)]['end']
            })
        
        # TODO: Use LLM to identify topic changes
        # For now, return chunks as-is
        return chunks

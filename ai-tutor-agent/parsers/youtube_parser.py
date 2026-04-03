"""
YouTube Video Parser using yt-dlp and Whisper
"""
import yt_dlp
import os
from typing import Dict, Optional
from pathlib import Path


class YouTubeParser:
    def __init__(self, whisper_model=None):
        self.supported_extensions = ['youtube', 'youtu.be']
        self.whisper_model = whisper_model
    
    def parse(self, url: str, output_dir: str = "./temp") -> Dict[str, any]:
        """
        Download YouTube video and extract audio/subtitles
        
        Returns:
            Dict with:
            - text: transcript text
            - metadata: video info
            - audio_path: path to audio file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'writesubtitles': True,
            'subtitleslangs': ['ru', 'en'],
            'writesubtitles': True,
            'skip_download': False,
        }
        
        video_info = None
        audio_path = None
        subtitles_text = ""
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_info = {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'url': url
            }
            
            # Get downloaded file path
            filename = ydl.prepare_filename(info)
            audio_path = filename.rsplit('.', 1)[0] + '.mp3'
            
            # Try to read subtitles if available
            subtitle_path = filename.rsplit('.', 1)[0] + '.vtt'
            if os.path.exists(subtitle_path):
                subtitles_text = self._parse_vtt(subtitle_path)
        
        # If no subtitles, use Whisper for transcription
        if not subtitles_text and self.whisper_model:
            from .audio_parser import AudioParser
            audio_parser = AudioParser(self.whisper_model)
            result = audio_parser.parse(audio_path)
            subtitles_text = result['text']
        
        return {
            'text': subtitles_text,
            'metadata': video_info,
            'audio_path': audio_path,
            'source': url,
            'type': 'youtube'
        }
    
    def _parse_vtt(self, vtt_path: str) -> str:
        """Parse VTT subtitle file"""
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove VTT timestamps and headers
        lines = []
        for line in content.split('\n'):
            if not line.startswith('WEBVTT') and not line.startswith('Kind:') and \
               not line.startswith('Language:') and '-->' not in line:
                if line.strip() and not line.isdigit():
                    lines.append(line.strip())
        
        return '\n'.join(lines)

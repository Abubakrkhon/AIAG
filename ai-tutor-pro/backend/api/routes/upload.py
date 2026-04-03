"""
Upload API - File upload and processing endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import os

router = APIRouter()


class UploadResponse(BaseModel):
    """Upload response model"""
    success: bool
    file_id: str
    filename: str
    file_type: str
    file_size: int
    message: str
    metadata: Dict[str, Any] = {}


ALLOWED_EXTENSIONS = {
    "pdf": ["application/pdf"],
    "docx": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "txt": ["text/plain"],
    "md": ["text/markdown", "text/x-markdown"],
    "mp3": ["audio/mpeg", "audio/mp3"],
    "wav": ["audio/wav"],
    "jpg": ["image/jpeg"],
    "png": ["image/png"],
    "webm": ["video/webm"],
    "mp4": ["video/mp4"]
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


@router.post("/file", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """
    Upload a file for processing.
    
    Supported formats: PDF, DOCX, TXT, MD, MP3, WAV, JPG, PNG
    """
    try:
        # Validate file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Get file extension
        ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        # Validate file type
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}"
            )
        
        # Generate file ID
        file_id = f"file_{uuid.uuid4().hex}"
        
        # Save file temporarily
        upload_dir = "./uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return UploadResponse(
            success=True,
            file_id=file_id,
            filename=file.filename,
            file_type=ext,
            file_size=file_size,
            message="File uploaded successfully",
            metadata={
                "description": description,
                "path": file_path
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/url")
async def upload_from_url(url: str, description: Optional[str] = None):
    """
    Upload content from URL (YouTube, web page, etc.)
    """
    try:
        # Detect URL type
        if "youtube.com" in url or "youtu.be" in url:
            source_type = "youtube"
        elif url.startswith("http"):
            source_type = "web"
        else:
            raise HTTPException(status_code=400, detail="Invalid URL")
        
        file_id = f"url_{uuid.uuid4().hex}"
        
        return {
            "success": True,
            "file_id": file_id,
            "source_type": source_type,
            "url": url,
            "message": f"{source_type} URL queued for processing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}")
async def get_file_info(file_id: str):
    """Get information about uploaded file"""
    # Placeholder - implement database lookup
    return {
        "success": True,
        "file_id": file_id,
        "status": "processed",
        "metadata": {}
    }


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete uploaded file"""
    # Placeholder - implement actual deletion
    return {
        "success": True,
        "message": f"File {file_id} deleted"
    }

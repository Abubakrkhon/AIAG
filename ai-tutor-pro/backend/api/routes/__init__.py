# API Routes
from .upload import router as upload_router
from .process import router as process_router
from .chat import router as chat_router
from .tests import router as tests_router
from .analytics import router as analytics_router

__all__ = [
    "upload_router",
    "process_router", 
    "chat_router",
    "tests_router",
    "analytics_router"
]

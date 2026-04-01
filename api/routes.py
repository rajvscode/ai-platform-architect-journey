from core.limiter import limiter
from core.models import LogRequest
from core.security import validate_api_key
from logger import logger
from cache import get_from_cache
from fastapi import APIRouter, Request, Header, BackgroundTasks
from service.worker import process_log_async
import time
import asyncio


router = APIRouter()

@router.post("/analyze-log")
@limiter.limit("5/minute")
async def analyze(
    request: Request,
    body: LogRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
    ):

    validate_api_key(x_api_key)

    start_time = time.time()

    logger.info(f"Incoming request: {body.log}")

    logger.info(f"Client IP: {request.client.host}")

    # 🔥 Step 1: Check cache
    cached = await asyncio.to_thread(get_from_cache, body.log)
    if cached:
        logger.info("Cache hit")
        return {"status": "completed", "data": cached}

    # 🔥 Add background task
    background_tasks.add_task(process_log_async, body.log, body.context)

    return {
        "status": "processing",
        "message": "Request accepted and processing in background"
    }

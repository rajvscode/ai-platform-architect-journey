from core.limiter import limiter
from core.models import LogRequest
from core.security import validate_api_key
from logger import logger
from cache import get_from_cache, save_to_cache
from fastapi import APIRouter, Request, Header
from rag import save_document
from service.analyzer import analyze_log
import time

router = APIRouter()

@router.post("/analyze-log")
@limiter.limit("5/minute")
def analyze(request: Request, body: LogRequest, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)

    start_time = time.time()

    logger.info(f"Incoming request: {body.log}")

    logger.info(f"Client IP: {request.client.host}")

    # 🔥 Step 1: Check cache
    cached = get_from_cache(body.log)
    if cached:
        logger.info("Cache hit")
        return cached

    try:
        result = analyze_log(body.log, body.context)

        # 🔥 Step 2: Save to cache
        save_to_cache(body.log, result)
        save_document(body.log)

        duration = time.time() - start_time

        logger.info(f"Response: {result}")
        logger.info(f"Execution time: {duration:.2f}s")

        return result

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": "Internal server error"}


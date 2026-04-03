from core.limiter import limiter
from core.models import LogRequest, DocumentRequest
from core.security import validate_api_key
from logger import logger
from cache import get_from_cache
from fastapi import APIRouter, Request, Header, BackgroundTasks
from service.worker import process_log_async
from result_store import save_result, get_result
from rag import save_document
import uuid
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
    job_id = str(uuid.uuid4())

    background_tasks.add_task(
        process_log_async,
        body.log,
        body.context,
        job_id
    )

    return {
        "status": "processing",
        "job_id": job_id
    }

@router.get("/result/{job_id}")
def fetch_result(job_id: str):
    result = get_result(job_id)

    if not result:
        return {"status": "processing"}

    return {
        "status": "completed",
        "data": result
    }

@router.post("/add-document")
def add_document(body: DocumentRequest, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)

    save_document(body.text)

    return {
        "status": "success",
        "message": "Document added to knowledge base"
    }
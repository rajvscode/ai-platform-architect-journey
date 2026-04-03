from core.limiter import limiter
from core.models import LogRequest, DocumentRequest
from core.security import validate_api_key
from logger import logger
from cache import get_from_cache
from fastapi import APIRouter, Request, Header, BackgroundTasks
from metrics import get_metrics, record_failure, record_feedback, record_latency, record_request, record_success
from service.worker import process_log_async
from result_store import save_feedback, save_result, get_result
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
    record_request()

    logger.info(f"Incoming request: {body.log}")
    logger.info(f"Client IP: {request.client.host}")

    try:
        # 🔥 Step 1: Check cache
        cached = await asyncio.to_thread(get_from_cache, body.log)
        if cached:
            logger.info("Cache hit")

            record_success()
            latency = time.time() - start_time
            record_latency(latency)

            return {"status": "completed", "data": cached}

        # 🔥 Step 2: Create job
        job_id = str(uuid.uuid4())

        # 🔥 Step 3: Background processing
        background_tasks.add_task(
            process_log_async,
            body.log,
            body.context,
            job_id
        )

        # 👉 IMPORTANT:
        # This is NOT success of processing, only acceptance
        latency = time.time() - start_time
        record_latency(latency)

        return {
            "status": "processing",
            "job_id": job_id
        }

    except Exception as e:
        logger.error(f"API failed: {str(e)}")

        record_failure()

        latency = time.time() - start_time
        record_latency(latency)

        return {"error": "Internal server error"}

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

    save_document(body.text, body.tag)

    return {
        "status": "success",
        "message": "Document added"
    }

@router.post("/feedback")
def add_feedback(job_id: str, feedback: str, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)

    save_feedback(job_id, feedback)

    record_feedback()

    return {
        "status": "success",
        "message": "Feedback stored"
    }

@router.get("/metrics")
def metrics_endpoint(x_api_key: str = Header(...)):
    validate_api_key(x_api_key)

    return get_metrics()
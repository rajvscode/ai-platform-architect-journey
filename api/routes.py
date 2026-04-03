from alerting import check_alerts
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

from fastapi.responses import HTMLResponse
from metrics import get_metrics


router = APIRouter()

@router.post("/analyze-log")
@limiter.limit("5/minute")
async def analyze(
    request: Request,
    body: LogRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    if x_api_key:
        validate_api_key(x_api_key)

    start_time = time.time()
    record_request()

    check_alerts()

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
def add_document(body: DocumentRequest, x_api_key: str = Header(None)):
    if x_api_key:
        validate_api_key(x_api_key)

    save_document(body.text, body.tag)

    return {
        "status": "success",
        "message": "Document added"
    }

@router.post("/feedback")
def add_feedback(job_id: str, feedback: str, x_api_key: str = Header(None)):
    if x_api_key:
        validate_api_key(x_api_key)

    save_feedback(job_id, feedback)

    record_feedback()

    return {
        "status": "success",
        "message": "Feedback stored"
    }

@router.get("/metrics")
def metrics_endpoint(x_api_key: str = Header(None)):
    if x_api_key:
        validate_api_key(x_api_key)

    return get_metrics()

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(x_api_key: str = Header(None)):
    if x_api_key:
        validate_api_key(x_api_key)

    data = get_metrics()

    html = f"""
    <html>
    <head>
        <title>AI Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>

        <h1>🚀 AI System Dashboard</h1>

        <p>Total Requests: <span id="total"></span></p>
        <p>Success: <span id="success"></span></p>
        <p>Failure: <span id="failure"></span></p>
        <p>Avg Latency: <span id="latency"></span></p>

        <h2>📈 Requests Over Time</h2>
        <canvas id="requestsChart"></canvas>

        <h2>⚡ Latency Trend</h2>
        <canvas id="latencyChart"></canvas>

        <script>
            async function loadMetrics() {{
                const res = await fetch('/metrics');
                const data = await res.json();

                document.getElementById('total').innerText = data.total_requests;
                document.getElementById('success').innerText = data.success;
                document.getElementById('failure').innerText = data.failure;
                document.getElementById('latency').innerText = data.average_latency;

                const labels = data.requests_timeline.map((_, i) => i + 1);

                requestsChart.data.labels = labels;
                requestsChart.data.datasets[0].data = labels;
                requestsChart.update();

                latencyChart.data.labels = labels;
                latencyChart.data.datasets[0].data = data.latencies;
                latencyChart.update();
            }}

            const requestsChart = new Chart(document.getElementById('requestsChart'), {{
                type: 'line',
                data: {{ labels: [], datasets: [{{ label: 'Requests', data: [] }}] }}
            }});

            const latencyChart = new Chart(document.getElementById('latencyChart'), {{
                type: 'line',
                data: {{ labels: [], datasets: [{{ label: 'Latency', data: [] }}] }}
            }});

            setInterval(loadMetrics, 5000);
            loadMetrics();
        </script>

    </body>
    </html>
    """

    return html
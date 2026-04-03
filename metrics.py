metrics = {
    "total_requests": 0,
    "successful_responses": 0,
    "failed_requests": 0,
    "feedback_count": 0,
    "total_latency": 0
}


def record_request():
    metrics["total_requests"] += 1


def record_success():
    metrics["successful_responses"] += 1


def record_failure():
    metrics["failed_requests"] += 1


def record_feedback():
    metrics["feedback_count"] += 1


def record_latency(latency):
    metrics["total_latency"] += latency


def get_metrics():
    avg_latency = 0
    if metrics["total_requests"] > 0:
        avg_latency = metrics["total_latency"] / metrics["total_requests"]

    return {
        **metrics,
        "average_latency": round(avg_latency, 2)
    }
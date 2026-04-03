metrics = {
    "requests": [],
    "latencies": [],
    "success": 0,
    "failure": 0,
    "feedback": 0
}


import time

def record_request():
    metrics["requests"].append(time.time())


def record_latency(latency):
    metrics["latencies"].append(latency)


def record_success():
    metrics["success"] += 1


def record_failure():
    metrics["failure"] += 1


def record_feedback():
    metrics["feedback"] += 1


def get_metrics():
    total_requests = len(metrics["requests"])

    avg_latency = 0
    if metrics["latencies"]:
        avg_latency = sum(metrics["latencies"]) / len(metrics["latencies"])

    return {
        "total_requests": total_requests,
        "success": metrics["success"],
        "failure": metrics["failure"],
        "feedback": metrics["feedback"],
        "average_latency": round(avg_latency, 2),
        "requests_timeline": metrics["requests"],
        "latencies": metrics["latencies"]
    }
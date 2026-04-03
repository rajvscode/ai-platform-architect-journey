from metrics import get_metrics
from logger import logger


def check_alerts():
    data = get_metrics()

    total = data["total_requests"]
    failures = data["failure"]
    latency = data["average_latency"]

    if total == 0:
        return

    failure_rate = failures / total

    # 🚨 Failure alert
    if failure_rate > 0.3:
        logger.error(f"🚨 ALERT: High failure rate! ({round(failure_rate*100,2)}%)")

    # 🚨 Latency alert
    if latency > 2:
        logger.warning(f"🚨 ALERT: High latency detected! ({latency}s)")
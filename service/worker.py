from cache import save_to_cache
from logger import logger
from rag import save_document
from result_store import save_result
from service.analyzer import analyze_log
import time


def process_log_async(log, context, job_id):
    logger.info(f"Processing job: {job_id}")

    result = analyze_log(log, context)

    save_to_cache(log, result)
    save_document(log)
    save_result(job_id, result)

    logger.info(f"Completed job: {job_id}")
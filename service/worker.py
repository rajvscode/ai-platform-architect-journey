from cache import save_to_cache
from logger import logger
from rag import save_document
from result_store import save_result
from service.analyzer import analyze_log
import time


def process_log_async(log, context, job_id):
    try:
        logger.info(f"Processing job: {job_id}")

        result = analyze_log(log, context)

        logger.info(f"LLM result received for job: {job_id}")

        save_to_cache(log, result)
        logger.info("Saved to cache")

        save_document(log, tag="payments")
        logger.info("Saved to memory")

        save_result(job_id, result)
        logger.info(f"Saved result for job: {job_id}")

        logger.info(f"Completed job: {job_id}")

    except Exception as e:
        logger.error(f"❌ Background job failed: {job_id}, Error: {str(e)}")
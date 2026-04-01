from cache import save_to_cache
from logger import logger
from rag import save_document
from service.analyzer import analyze_log
import time


def process_log_async(log, context):
    logger.info(f"Background processing started: {log}")

    result = analyze_log(log, context)

    save_to_cache(log, result)
    save_document(log)

    logger.info(f"Background processing completed: {log}")
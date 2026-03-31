from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from rag import search_similar
from rag import search_similar, save_document
from logger import logger
from cache import get_from_cache, save_to_cache
import time
import os
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LogRequest(BaseModel):
    log: str
    context: list[str] = []


def analyze_log(log_text, context_logs):
    retrieved_docs = search_similar(log_text, threshold=0.8)

    if not retrieved_docs:
        retrieved_docs = ["No relevant past logs found"]

    print("Retrieved Docs:", retrieved_docs)

    context_text = "\n".join(context_logs)
    memory_text = "\n".join(retrieved_docs)


    prompt = f"""
You are a senior backend engineer expert in Kafka, distributed systems, and payments.

Use both system context and retrieved knowledge.

Return STRICTLY valid JSON:

{{
  "issue": "short description",
  "root_causes": ["cause1", "cause2"],
  "solutions": ["solution1", "solution2"]
}}

Knowledge Base (only relevant past issues):
{memory_text}

Context Logs:
{context_text}

Current Log:
{log_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"error": "Invalid JSON", "raw": content}


@app.post("/analyze-log")
def analyze(request: LogRequest):
    start_time = time.time()

    logger.info(f"Incoming request: {request.log}")

    # 🔥 Step 1: Check cache
    cached = get_from_cache(request.log)
    if cached:
        logger.info("Cache hit")
        return cached

    try:
        result = analyze_log(request.log, request.context)

        # 🔥 Step 2: Save to cache
        save_to_cache(request.log, result)

        duration = time.time() - start_time

        logger.info(f"Response: {result}")
        logger.info(f"Execution time: {duration:.2f}s")

        save_document(request.log)

        return result

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": "Internal server error"}
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LogRequest(BaseModel):
    log: str


def analyze_log(log_text):
    prompt = f"""
You are a senior backend engineer expert in Kafka, distributed systems, and payments.

Return STRICTLY valid JSON:

{{
  "issue": "short description",
  "root_causes": ["cause1", "cause2"],
  "solutions": ["solution1", "solution2"]
}}

Log:
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
    return analyze_log(request.log)
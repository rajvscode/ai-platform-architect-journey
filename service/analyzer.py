from core.config import client
from rag import search_similar, save_document
import json

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

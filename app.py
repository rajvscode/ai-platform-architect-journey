from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_log(log_text):
    prompt = f"""
You are a senior backend engineer expert in Kafka, distributed systems, and payments.

Return STRICTLY valid JSON. Do not add explanations or text outside JSON.

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
        parsed = json.loads(content)
        return parsed
    except:
        return {"error": "Invalid JSON from model", "raw_output": content}


if __name__ == "__main__":
    log = input("Enter your log: ")
    result = analyze_log(log)

    print("\n--- Structured Analysis ---\n")
    print(json.dumps(result, indent=2))
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_log(log_text):
    prompt = f"""
You are a senior backend engineer.

Analyze the following log and provide:
1. What the issue is
2. Possible root causes
3. Suggested fixes

Log:
{log_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    log = input("Enter your log: ")
    result = analyze_log(log)
    print("\n--- Analysis ---\n")
    print(result)
from core.config import client


def detect_tag(log_text):
    prompt = f"""
Classify the following log into one category:

Categories:
- payments
- kafka
- database
- network
- general

Return ONLY the category name.

Log:
{log_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    tag = response.choices[0].message.content.strip().lower()

    return tag
import os, json
from openai import OpenAI

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

def draft_outline(topic: str, text: str | None = None):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Bạn là trợ lý tạo slide. Chủ đề: {topic}
{text if text else ""}

Yêu cầu:
- Tạo dàn ý tối đa 12 slide.
- Mỗi slide gồm: title, bullets (3-5 gạch đầu dòng ngắn), notes (1-2 câu).
- Trả JSON: [{{"title":"","bullets":[""],"notes":""}}, ...]
"""
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.4,
    )
    content = resp.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        # try to extract JSON block
        import re
        m = re.search(r'\[.*\]', content, re.S)
        data = json.loads(m.group(0)) if m else []
    return data

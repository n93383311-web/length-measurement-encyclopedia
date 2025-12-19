import json
import os
import requests

API_KEY = os.environ.get("AI_API_KEY")
if not API_KEY:
    raise RuntimeError("AI_API_KEY not set")

OUTPUT_DIR = "data/encyclopedia"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("data/index.json", "r", encoding="utf-8") as f:
    index = json.load(f)

def ai_write(prompt):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are writing a scientific encyclopedia. Use formal, neutral, academic style."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

for topic in index["topics"]:
    title = topic["title"]
    filename = title.lower().replace(" ", "_") + ".md"
    path = os.path.join(OUTPUT_DIR, filename)

    content = f"# {title}\n\n"

    for section in topic["sections"]:
        prompt = f"""
Write an encyclopedia section titled "{section}" for the topic "{title}".
Use SI units, historical accuracy, and formal scientific tone.
"""
        text = ai_write(prompt)
        content += f"## {section}\n\n{text}\n\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Written: {path}")

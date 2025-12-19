import requests
import os

TOPICS = {
    "Length": "definition",
    "Distance": "definition",
    "Metre": "units",
    "Vernier_caliper": "instruments",
    "Measurement_error": "errors"
}

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "LengthMeasurementBot/1.0 (https://github.com/n93383311-web/length-measurement-encyclopedia)"
}

BASE_DIR = "data/wikipedia"

os.makedirs(BASE_DIR, exist_ok=True)

for title, category in TOPICS.items():
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": title
    }

    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()

    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    text = page.get("extract", "").strip()

    if not text:
        continue

    filename = f"{category}_{title.lower().replace(' ', '_')}.md"
    path = os.path.join(BASE_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{text}")

    print(f"Saved: {path}")

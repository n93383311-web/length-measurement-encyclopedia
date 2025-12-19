import requests

API_URL = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "explaintext": True,
    "titles": "Length"
}

HEADERS = {
    "User-Agent": "LengthMeasurementBot/1.0 (https://github.com/YOUR_USERNAME/length-measurement-encyclopedia)"
}

response = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
response.raise_for_status()

data = response.json()

page = next(iter(data["query"]["pages"].values()))
text = page.get("extract", "")

output = "# Measurement of Length\n\n" + text

with open("data/wikipedia/length_measurement.md", "w", encoding="utf-8") as f:
    f.write(output)

print("Wikipedia API content saved.")

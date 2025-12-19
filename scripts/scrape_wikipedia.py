import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Length"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

content = soup.find("div", {"id": "mw-content-text"})

text = []
for p in content.find_all("p"):
    t = p.get_text().strip()
    if t:
        text.append(t)

output = "# Measurement of Length\n\n" + "\n\n".join(text)

with open("data/wikipedia/length_measurement.md", "w", encoding="utf-8") as f:
    f.write(output)

print("Wikipedia length page scraped.")

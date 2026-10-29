import os

import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TANKERKOENIG_API_KEY")

url = "https://creativecommons.tankerkoenig.de/json/list.php"
params = {
    "lat": 52.52,
    "lng": 13.405,
    "rad": 2,
    "sort": "price",
    "type": "diesel",
    "apikey": api_key,
}

antwort = httpx.get(url, params=params)
daten = antwort.json()

for tankstelle in daten["stations"]:
    print(tankstelle["name"], tankstelle["price"])
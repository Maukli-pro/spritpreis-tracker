import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TANKERKOENIG_API_KEY")
BASIS_URL = "https://creativecommons.tankerkoenig.de/json/list.php"


def tankstellen_suchen(lat: float, lng: float, radius: float, sorte: str) -> list[dict]:
    params = {
        "lat": lat,
        "lng": lng,
        "rad": radius,
        "sort": "price",
        "type": sorte,
        "apikey": API_KEY,
    }
    antwort = httpx.get(BASIS_URL, params=params, timeout=10)
    antwort.raise_for_status()
    daten = antwort.json()

    if not daten.get("ok"):
        raise RuntimeError(daten.get("message", "Unbekannter Fehler bei Tankerkönig"))

    ergebnis = []
    for t in daten["stations"]:
        ergebnis.append({
            "name": t["name"],
            "marke": t["brand"],
            "adresse": f'{t["street"]} {t["houseNumber"] or ""}'.strip(),
            "ort": f'{t["postCode"]} {t["place"]}',
            "entfernung_km": t["dist"],
            "preis": t["price"],
            "geoeffnet": t["isOpen"],
        })
    return ergebnis
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
    }

    stationen = _anfrage_senden(params)

    ergebnis = []
    for t in stationen:
        ergebnis.append({
            "id": t["id"],
            "name": t["name"],
            "marke": t["brand"],
            "adresse": f'{t["street"]} {t["houseNumber"] or ""}'.strip(),
            "ort": f'{t["postCode"]} {t["place"]}',
            "entfernung_km": t["dist"],
            "preis": t["price"],
            "geoeffnet": t["isOpen"],
            "lat": t["lat"],
            "lng": t["lng"],
        })

    return ergebnis



def _anfrage_senden(params: dict) -> list[dict]:
    alle_params = {**params, "apikey": API_KEY}
    antwort = httpx.get(BASIS_URL, params=alle_params, timeout=10)
    antwort.raise_for_status()
    daten = antwort.json()

    if not daten.get("ok"):
        raise RuntimeError(daten.get("message", "Unbekannter Fehler bei Tankerkönig"))

    return daten["stations"]
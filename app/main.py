from typing import Annotated, Literal

import httpx
from fastapi import FastAPI, HTTPException, Query

from app.tankerkoenig import tankstellen_suchen

app = FastAPI()


@app.get("/")
def startseite():
    return {"nachricht": "Spritpreis-Tracker läuft"}


@app.get("/preise")
def preise_abfragen(
    lat: Annotated[float, Query(ge=47.2, le=55.1, description="Breitengrad")],
    lng: Annotated[float, Query(ge=5.8, le=15.1, description="Längengrad")],
    radius: Annotated[float, Query(gt=0, le=25, description="Suchradius in km")] = 5,
    sorte: Literal["e5", "e10", "diesel"] = "diesel",
):
    try:
        tankstellen = tankstellen_suchen(lat, lng, radius, sorte)
    except (httpx.HTTPError, RuntimeError):
        raise HTTPException(status_code=502, detail="Spritpreise konnten gerade nicht abgerufen werden")

    return {"sorte": sorte, "anzahl": len(tankstellen), "tankstellen": tankstellen}
    
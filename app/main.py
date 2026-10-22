from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def startseite():
    return {"nachricht": "Spritpreis-Tracker läuft"}

@app.get("/preis/{sorte}")
def preis_abfragen(sorte: str):
    preis = 1.799
    return {"sorte": sorte, "preis": preis}
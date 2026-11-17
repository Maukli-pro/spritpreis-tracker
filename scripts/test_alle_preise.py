from app.tankerkoenig import alle_preise_abrufen

ergebnis = alle_preise_abrufen(
    lat=52.5200,
    lng=13.4049,
    radius=25,
)

print("Anzahl der Tankstellen:", len(ergebnis))
print("Erste Tankstelle:", ergebnis[0])
# Entscheidungen

## FastAPI statt Flask oder Django
Ich habe FastAPI gewählt, weil es Python ist und Python die Standardsprache für Data Science ist. FastAPI wird oft genutzt, um ML-Modelle als API bereitzustellen, und genau das plane ich später für die Preisvorhersage.
Außerdem prüft FastAPI Eingaben automatisch anhand der Typen (ungültige Werte bekommen einen 422-Fehler) und erzeugt unter /docs eine Dokumentation, mit der man jeden Endpunkt direkt testen kann. Flask bietet beides nicht von Haus aus, und Django wäre für eine reine API zu groß.

## Tankerkönig als Datenquelle
Tankstellen in Deutschland müssen ihre Preise für E5, E10 und Diesel gesetzlich an die Markttransparenzstelle für Kraftstoffe (MTS-K) des Bundeskartellamts melden. Tankerkönig stellt diese offiziellen Daten kostenlos über eine API bereit. Damit sind sie verlässlicher als zum Beispiel die Preise in Google Maps.
Einschränkungen: Premium-Sorten wie V-Power gibt es nicht, weil sie nicht meldepflichtig sind. Die API ist nicht für massenhaftes Abfragen gedacht, deshalb frage ich sparsam ab. Die Daten stehen unter der Lizenz CC BY 4.0, deshalb muss ich die Quelle in der App angeben.

## Code in eigene Dateien aufgeteilt
main.py beschreibt nur die Endpunkte. Die Kommunikation mit Tankerkönig liegt in tankerkoenig.py, die Datenbank in database.py und models.py. So kann ich eine Funktion an mehreren Stellen nutzen, zum Beispiel später für die Suche per Standort und per Postleitzahl, und jeden Teil einzeln testen oder austauschen.
Mein Endpunkt gibt ein eigenes Format mit deutschen Feldnamen zurück statt der Rohdaten von Tankerkönig. Wenn ich die Datenquelle wechsle, bleibt die Schnittstelle für das Frontend gleich.

## API-Schlüssel in einer .env-Datei
Der Schlüssel steht nicht im Code, sondern in der .env-Datei, die durch die .gitignore nie auf GitHub landet. Sonst könnte jeder meinen Schlüssel auslesen und benutzen.
Bekomme ich einen neuen Schlüssel, ändere ich nur die .env und nicht den Code. Auf dem Server setze ich später dieselbe Variable in den Einstellungen.

## SQLite und SQLAlchemy
SQLite ist nur eine Datei und braucht keinen eigenen Datenbankserver. Das ist ideal für den Anfang.
SQLAlchemy ist ein ORM: Ich beschreibe die Tabellen als Python-Klassen, statt SQL von Hand zu schreiben. Der große Vorteil: Wenn ich später auf PostgreSQL wechsle, zum Beispiel beim Online-Stellen, ändere ich nur die DATABASE_URL, der restliche Code bleibt gleich. Deshalb habe ich am Anfang keinen MySQL-Server aufgesetzt.

## Zwei Tabellen statt einer
Name, Adresse und Koordinaten einer Tankstelle ändern sich fast nie, die Preise dagegen mehrmals am Tag. In einer einzigen Tabelle stünden die Tankstellendaten bei jeder Preismessung erneut, also tausendfach doppelt. Das kostet Platz und kann zu Widersprüchen führen, wenn sich zum Beispiel eine Adresse ändert.
Deshalb habe ich die Daten normalisiert: eine Tabelle tankstellen und eine Tabelle preise, verbunden über tankstelle_id als Fremdschlüssel (1:n-Beziehung).

## 25 km Radius und 15 Minuten
Tankerkönig liefert mit einer einzigen Anfrage alle Tankstellen im Umkreis von bis zu 25 km, mit allen drei Sorten. Eine Anfrage mit 25 km kostet genauso viel wie eine mit 15 km, deshalb nehme ich das Maximum. So ist fast ganz Berlin abgedeckt.
Bei einer Messung alle 15 Minuten sind das nur 96 Anfragen am Tag. Die Auflösung reicht, um die typischen Preisschwankungen über den Tag zu erkennen, die ich später für die Vorhersage brauche. Orte außerhalb dieses Bereichs werden live auf Anfrage abgefragt.
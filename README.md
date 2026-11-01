# Pac-Man · Python Arcade

Ein im Browser spielbares Pac-Man-Fanprojekt. Die vollständige Spiellogik läuft in Python über Pyodide (WebAssembly). JavaScript übernimmt Canvas-Darstellung und Eingaben.

## Starten

Python 3.10 oder neuer, keine pip-Pakete erforderlich:

```sh
python server.py
```

Dann http://localhost:8000 öffnen. Beim ersten Laden ist Internet für die Pyodide-Laufzeit erforderlich. Die Seite lädt außerdem optionale Google Fonts. Nicht mit file:// öffnen.

## Steuerung

- Pfeiltasten oder WASD: bewegen
- Enter: starten
- Leertaste: Pause / fortsetzen
- Mobil: Bildschirmtasten oder Wischgesten

Drei Leben, vier Geister, Power-Pellets, fortlaufende Level und lokaler Highscore. Richtungswechsel werden gepuffert. Der Highscore bleibt im jeweiligen Browser gespeichert.

## Struktur

- `dist/game.py`: Python-Spiellogik, auch mit CPython testbar
- `dist/index.html`: responsive Oberfläche und Pyodide-Anbindung
- `server.py`: lokaler Webserver mit Python-Standardbibliothek
- `test_game.py`: Tests für Labyrinth, Bewegung, Kollisionen, Power-Pellets und Level

```sh
python -m unittest -v
```

Die gehostete Version besteht aus den Dateien in `dist/`. Es werden keine Spielstände an einen Server gesendet. Dies ist ein inoffizielles Lernprojekt ohne originale Spielgrafiken oder Audiodateien; Pac-Man ist eine Marke von Bandai Namco.

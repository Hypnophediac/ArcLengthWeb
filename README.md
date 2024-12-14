# Lemez Hajlítás Kalkulátor

Ez a program egy grafikus felületű kalkulátor lemezek hajlításának tervezéséhez. A program segítségével kiszámíthatók és vizualizálhatók a hajlítási paraméterek.

## Funkciók

- Különböző anyagok kezelése előre definiált K-faktorokkal
- Belső, semleges és külső sugár számítása
- Hajlítási szögek és kiegészítő szögek megjelenítése
- Húrhosszak számítása és megjelenítése
- Interaktív vizualizáció zoom és pan funkciókkal
- Kezdő és záró egyenes szakaszok kezelése

## Telepítés

1. Klónozza le a repository-t
2. Telepítse a szükséges függőségeket:
```bash
pip install -r requirements.txt
```

## Használat

1. Indítsa el a programot:
```bash
python main.py
```

2. A program használata:
   - Válasszon anyagot a legördülő listából
   - Válassza ki a sugár típusát (belső, semleges vagy külső)
   - Adja meg a szükséges paramétereket:
     - Sugár értéke (mm)
     - Lemezvastagság (mm)
     - K-faktor (alapértelmezett érték az anyag alapján)
     - Hajlítások száma
     - Teljes hajlítási szög (°)
     - Kezdő és záró egyenes szakaszok hossza (mm)
   - Kattintson a "Számítás" gombra

3. Vizualizáció kezelése:
   - Nagyítás/kicsinyítés: egérgörgő
   - Eltolás: bal egérgomb nyomva tartása és húzás

## Fájlok struktúrája

- `main.py` - A program belépési pontja
- `gui.py` - Grafikus felület implementációja
- `drawing.py` - Rajzolási funkciók
- `calculations.py` - Számítási műveletek
- `config.py` - Konfigurációs beállítások
- `material_database.py` - Anyagok adatbázisa

## Fejlesztői információk

A program moduláris felépítésű, az egyes funkciók külön fájlokban vannak implementálva a könnyebb karbantarthatóság és továbbfejleszthetőség érdekében.

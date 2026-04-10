import json


def wczytaj_konfiguracje(sciezka="config.json"):
    with open(sciezka, "r", encoding="utf-8") as plik:
        return json.load(plik)
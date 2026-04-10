import json
import os


def zapisz_raport_json(dane):
    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w", encoding="utf-8") as plik:
        json.dump(dane, plik, indent=4, ensure_ascii=False)
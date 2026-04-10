import psutil


def pobierz_status_uslugi(nazwa_uslugi):
    try:
        usluga = psutil.win_service_get(nazwa_uslugi)
        dane = usluga.as_dict()

        return {
            "nazwa": nazwa_uslugi,
            "display_name": dane.get("display_name"),
            "status": dane.get("status"),
            "start_type": dane.get("start_type"),
            "binpath": dane.get("binpath")
        }
    except Exception as blad:
        return {
            "nazwa": nazwa_uslugi,
            "status": "not_found",
            "blad": str(blad)
        }


def sprawdz_uslugi(lista_uslug):
    wyniki = []

    for nazwa_uslugi in lista_uslug:
        wyniki.append(pobierz_status_uslugi(nazwa_uslugi))

    return wyniki
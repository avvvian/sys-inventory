from modules.system_info import pobierz_informacje_systemowe
from modules.health_check import pobierz_stan_systemu
from modules.service_check import sprawdz_uslugi
from modules.network_check import sprawdz_hosty, sprawdz_porty
from modules.report_writer import zapisz_raport_json
from modules.config_loader import wczytaj_konfiguracje


def main():
    konfiguracja = wczytaj_konfiguracje()

    informacje_systemowe = pobierz_informacje_systemowe()
    stan_systemu = pobierz_stan_systemu(konfiguracja["progi"])
    uslugi = sprawdz_uslugi(konfiguracja["monitorowane_uslugi"])
    hosty = sprawdz_hosty(konfiguracja["hosty_do_sprawdzenia"])
    porty = sprawdz_porty(konfiguracja["porty_do_sprawdzenia"])

    raport = {
        "informacje_systemowe": informacje_systemowe,
        "stan_systemu": stan_systemu,
        "uslugi": uslugi,
        "hosty": hosty,
        "porty": porty
    }

    zapisz_raport_json(raport)
    print("Raport został zapisany do pliku reports/report.json")


if __name__ == "__main__":
    main()
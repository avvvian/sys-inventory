from modules.system_info import pobierz_informacje_systemowe
from modules.health_check import pobierz_stan_systemu
from modules.report_writer import zapisz_raport_json


def main():
    informacje_systemowe = pobierz_informacje_systemowe()
    stan_systemu = pobierz_stan_systemu()

    raport = {
        "informacje_systemowe": informacje_systemowe,
        "stan_systemu": stan_systemu
    }

    zapisz_raport_json(raport)
    print("Raport został zapisany do pliku reports/report.json")


if __name__ == "__main__":
    main()
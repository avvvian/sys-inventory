import psutil
from datetime import datetime


def pobierz_czas_startu_systemu():
    czas_startu = datetime.fromtimestamp(psutil.boot_time())
    return czas_startu.strftime("%Y-%m-%d %H:%M:%S")


def pobierz_stan_systemu():
    pamiec = psutil.virtual_memory()
    dysk = psutil.disk_usage("/")

    stan = {
        "cpu_procent": psutil.cpu_percent(interval=1),
        "ram_procent": pamiec.percent,
        "ram_calkowita_gb": round(pamiec.total / (1024 ** 3), 2),
        "ram_dostepna_gb": round(pamiec.available / (1024 ** 3), 2),
        "dysk_procent": dysk.percent,
        "dysk_calkowity_gb": round(dysk.total / (1024 ** 3), 2),
        "dysk_wolny_gb": round(dysk.free / (1024 ** 3), 2),
        "czas_startu_systemu": pobierz_czas_startu_systemu(),
        "czas_wygenerowania_raportu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return stan
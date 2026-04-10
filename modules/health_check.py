import psutil
from datetime import datetime


def pobierz_czas_startu_systemu():
    czas_startu = datetime.fromtimestamp(psutil.boot_time())
    return czas_startu.strftime("%Y-%m-%d %H:%M:%S")


def okresl_poziom(procent):
    if procent >= 90:
        return "critical"
    elif procent >= 75:
        return "warning"
    else:
        return "healthy"


def okresl_status_komputera(cpu_procent, ram_procent, najwyzszy_dysk_procent):
    poziomy = [
        okresl_poziom(cpu_procent),
        okresl_poziom(ram_procent),
        okresl_poziom(najwyzszy_dysk_procent)
    ]

    if "critical" in poziomy:
        return "critical"
    elif "warning" in poziomy:
        return "warning"
    else:
        return "healthy"


def pobierz_dyski():
    lista_dyskow = []
    partycje = psutil.disk_partitions()

    for partycja in partycje:
        try:
            uzycie = psutil.disk_usage(partycja.mountpoint)

            dane_dysku = {
                "urzadzenie": partycja.device,
                "punkt_montowania": partycja.mountpoint,
                "system_plikow": partycja.fstype,
                "procent_uzycia": uzycie.percent,
                "calkowity_gb": round(uzycie.total / (1024 ** 3), 2),
                "wolny_gb": round(uzycie.free / (1024 ** 3), 2),
                "status": okresl_poziom(uzycie.percent)
            }

            lista_dyskow.append(dane_dysku)
        except PermissionError:
            continue

    return lista_dyskow


def pobierz_stan_systemu():
    pamiec = psutil.virtual_memory()
    cpu_procent = psutil.cpu_percent(interval=1)
    ram_procent = pamiec.percent
    dyski = pobierz_dyski()

    if dyski:
        najwyzszy_dysk_procent = max(dysk["procent_uzycia"] for dysk in dyski)
    else:
        najwyzszy_dysk_procent = 0

    stan = {
        "cpu_procent": cpu_procent,
        "ocena_cpu": okresl_poziom(cpu_procent),

        "ram_procent": ram_procent,
        "ram_calkowita_gb": round(pamiec.total / (1024 ** 3), 2),
        "ram_dostepna_gb": round(pamiec.available / (1024 ** 3), 2),
        "ocena_ram": okresl_poziom(ram_procent),

        "czas_startu_systemu": pobierz_czas_startu_systemu(),
        "czas_wygenerowania_raportu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "dyski": dyski,
        "status_komputera": okresl_status_komputera(cpu_procent, ram_procent, najwyzszy_dysk_procent)
    }

    return stan
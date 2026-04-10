import psutil
from datetime import datetime


def pobierz_czas_startu_systemu():
    czas_startu = datetime.fromtimestamp(psutil.boot_time())
    return czas_startu.strftime("%Y-%m-%d %H:%M:%S")


def okresl_poziom(procent, prog_warning, prog_critical):
    if procent >= prog_critical:
        return "critical"
    elif procent >= prog_warning:
        return "warning"
    else:
        return "healthy"


def zbuduj_powod(typ, element, procent, prog_warning, prog_critical):
    status = okresl_poziom(procent, prog_warning, prog_critical)

    if status == "healthy":
        return None

    if status == "warning":
        opis = f"{typ} {element} osiągnął {procent}% - przekroczono próg warning ({prog_warning}%)"
        sugestia = "Warto obserwować ten zasób"
    else:
        opis = f"{typ} {element} osiągnął {procent}% - przekroczono próg critical ({prog_critical}%)"
        sugestia = "Może być potrzebna interwencja"

    return {
        "typ": typ,
        "element": element,
        "status": status,
        "wartosc_procent": procent,
        "opis": opis,
        "sugestia": sugestia
    }


def pobierz_dyski(progi_dysku):
    lista_dyskow = []
    powody = []

    partycje = psutil.disk_partitions()

    for partycja in partycje:
        try:
            uzycie = psutil.disk_usage(partycja.mountpoint)
            procent = uzycie.percent
            status = okresl_poziom(
                procent,
                progi_dysku["warning"],
                progi_dysku["critical"]
            )

            dane_dysku = {
                "urzadzenie": partycja.device,
                "punkt_montowania": partycja.mountpoint,
                "system_plikow": partycja.fstype,
                "procent_uzycia": procent,
                "calkowity_gb": round(uzycie.total / (1024 ** 3), 2),
                "wolny_gb": round(uzycie.free / (1024 ** 3), 2),
                "status": status
            }

            lista_dyskow.append(dane_dysku)

            powod = zbuduj_powod(
                "Dysk",
                partycja.mountpoint,
                procent,
                progi_dysku["warning"],
                progi_dysku["critical"]
            )
            if powod:
                powody.append(powod)

        except PermissionError:
            continue

    return lista_dyskow, powody


def pobierz_stan_systemu(progi):
    pamiec = psutil.virtual_memory()
    cpu_procent = psutil.cpu_percent(interval=1)
    ram_procent = pamiec.percent

    ocena_cpu = okresl_poziom(
        cpu_procent,
        progi["cpu"]["warning"],
        progi["cpu"]["critical"]
    )
    ocena_ram = okresl_poziom(
        ram_procent,
        progi["ram"]["warning"],
        progi["ram"]["critical"]
    )

    dyski, powody_dyskow = pobierz_dyski(progi["dysk"])

    powody_statusu = []

    powod_cpu = zbuduj_powod(
        "CPU",
        "Procesor",
        cpu_procent,
        progi["cpu"]["warning"],
        progi["cpu"]["critical"]
    )
    if powod_cpu:
        powody_statusu.append(powod_cpu)

    powod_ram = zbuduj_powod(
        "RAM",
        "Pamięć RAM",
        ram_procent,
        progi["ram"]["warning"],
        progi["ram"]["critical"]
    )
    if powod_ram:
        powody_statusu.append(powod_ram)

    powody_statusu.extend(powody_dyskow)

    wszystkie_statusy = [ocena_cpu, ocena_ram] + [dysk["status"] for dysk in dyski]

    if "critical" in wszystkie_statusy:
        status_komputera = "critical"
    elif "warning" in wszystkie_statusy:
        status_komputera = "warning"
    else:
        status_komputera = "healthy"

    stan = {
        "cpu_procent": cpu_procent,
        "ocena_cpu": ocena_cpu,
        "ram_procent": ram_procent,
        "ram_calkowita_gb": round(pamiec.total / (1024 ** 3), 2),
        "ram_dostepna_gb": round(pamiec.available / (1024 ** 3), 2),
        "ocena_ram": ocena_ram,
        "czas_startu_systemu": pobierz_czas_startu_systemu(),
        "czas_wygenerowania_raportu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dyski": dyski,
        "status_komputera": status_komputera,
        "powody_statusu": powody_statusu
    }

    return stan
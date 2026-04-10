import subprocess
import socket
import platform


def ping_host(host):
    system = platform.system().lower()

    if system == "windows":
        komenda = ["ping", "-n", "1", host]
    else:
        komenda = ["ping", "-c", "1", host]

    wynik = subprocess.run(
        komenda,
        capture_output=True,
        text=True
    )

    return {
        "host": host,
        "online": wynik.returncode == 0
    }


def sprawdz_hosty(lista_hostow):
    wyniki = []

    for host in lista_hostow:
        wyniki.append(ping_host(host))

    return wyniki


def sprawdz_port(host, port, timeout=2):
    gniazdo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gniazdo.settimeout(timeout)

    try:
        wynik = gniazdo.connect_ex((host, port))
        otwarty = wynik == 0
    except Exception:
        otwarty = False
    finally:
        gniazdo.close()

    return {
        "host": host,
        "port": port,
        "open": otwarty
    }


def sprawdz_porty(lista_portow):
    wyniki = []

    for element in lista_portow:
        host = element["host"]
        port = element["port"]
        wyniki.append(sprawdz_port(host, port))

    return wyniki
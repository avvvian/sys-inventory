import platform
import socket
import getpass
import os


def pobierz_adres_ip():
    try:
        nazwa_hosta = socket.gethostname()
        adres_ip = socket.gethostbyname(nazwa_hosta)
        return adres_ip
    except:
        return "Nie udało się pobrać adresu IP"


def pobierz_informacje_systemowe():
    informacje = {
        "nazwa_komputera": socket.gethostname(),
        "uzytkownik": getpass.getuser(),
        "system": platform.system(),
        "wersja_systemu": platform.version(),
        "release_systemu": platform.release(),
        "architektura": platform.machine(),
        "adres_ip": pobierz_adres_ip(),
        "katalog_roboczy": os.getcwd()
    }

    return informacje
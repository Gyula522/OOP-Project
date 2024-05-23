from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# 1. Szoba absztakt osztály
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def get_ar(self):
    #Visszaadja a szoba árát.
        pass

# 2. Szoba osztályból származtatott EgyágyasSzoba és KétágyasSzoba osztályok
class EgyagyasSzoba(Szoba):
    def get_ar(self):
        return self.ar

class KetagyasSzoba(Szoba):
    def get_ar(self):
        return self.ar

# 3. Szálloda osztály, amely szobákból áll és van neve
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

# 4. Foglalás osztály, amelyben a Szálloda foglalásait tároljuk
class Foglalas:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = {}

# 5. Szobák  foglalása metódus dátum alapján, visszaadja annak árát
    def foglal(self, szobaszam, datum):

# 9. Annak ellenőrzése, hogy a foglalás jövőbeni és a szoba szabad.
        if datum < datetime.now().date():
            return "Nem tud szobát foglalni a mai napnál régebbi időpontra."
        if (szobaszam, datum) in self.foglalasok:
            return "A lefoglalni kívánt szoba a megadott napra már foglalt. Kérjük válasszon másik szobát vagy napot."
        for szoba in self.szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                self.foglalasok[(szobaszam, datum)] = szoba
                return f"Sikeres szobafoglalás. Ár: {szoba.get_ar()} Ft"
        return "A megadott szobaszám nincs a rendszerben. Kérjük ellenőrizze a megadott szobaszámot."

# 6. A foglalás lemondását lehetővé tevő metódus
    def lemondas(self, szobaszam, datum):

# 10. Lemondás csak létező foglalásra lehetséges
        if (szobaszam, datum) in self.foglalasok:
            del self.foglalasok[(szobaszam, datum)]
            return "Szobafoglalás sikeres lemondása."
        return "A megadott adatokhoz nem tartozik szobafoglalás a rendszerünkben. Kérjük ellenőrizze a megadott adatokat."

# 7. Metódus, amely listázza a foglalásokat
    def foglalasok_listazasa(self):
        """Összes foglalás listázása."""
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return '\n'.join([f"Szobaszám: {key[0]}, Dátum: {key[1]}" for key in self.foglalasok])

# 11. Rendszer feltöltése 1 szállodával, 3 szobával és 5 szobafoglalással a felhasználói adatbekérés előtt.
szalloda = Szalloda("OOP Projektszálló")
szalloda.szoba_hozzaad(EgyagyasSzoba(30000, 101))
szalloda.szoba_hozzaad(KetagyasSzoba(45000, 102))
szalloda.szoba_hozzaad(KetagyasSzoba(45000, 103))

foglalas_kezelo = Foglalas(szalloda)
foglalas_kezelo.foglal(101, datetime.now().date() + timedelta(days=10))
foglalas_kezelo.foglal(102, datetime.now().date() + timedelta(days=10))
foglalas_kezelo.foglal(103, datetime.now().date() + timedelta(days=10))
foglalas_kezelo.foglal(101, datetime.now().date() + timedelta(days=11))
foglalas_kezelo.foglal(102, datetime.now().date() + timedelta(days=11))

# 8. Egyszerű felhasználói interfész, ahol a felhasználó kiválaszthatja a kívánt műveletet
def Szobafoglalas():
    while True:
        print("\nÜdvözöljük a szobafoglalási rendszerünkben! Kérjük válasszon az alábbi műveletek közül:")
        print("Szoba foglalása - 1 ")
        print("Szobafoglalás lemondása - 2 ")
        print("Szobafoglalások listázása - 3 ")
        print("Kilépés a rendszerből - 4 ")
        valasztas = input("Kérem adja meg a választott művelet számát: ")

        if valasztas == "1":
            szobaszam = int(input("Adja meg a lefoglalni kívánt szoba számát (Egyágyas szobánk a 101-es, Kétágyas szobáink a 102-es és a 103-as): "))
            datum = input("Adja meg, melyik napra kíván szobát foglalni (ÉÉÉÉ.HH.NN formátumban): ")
            try:
                datum = datetime.strptime(datum, "%Y.%m.%d").date()
            except ValueError:
                print("Hibás dátumformátum! Kérjük használja az ÉÉÉÉ.HH.NN formátumot.")
                continue
            eredmeny = foglalas_kezelo.foglal(szobaszam, datum)
            print(eredmeny)

        elif valasztas == "2":
            szobaszam = int(input("Adja meg a lefoglalt szoba számát: "))
            datum = input("Adja meg a lefoglalt dátumot (ÉÉÉÉ.HH.NN formátumban): ")
            try:
                datum = datetime.strptime(datum, "%Y.%m.%d").date()
            except ValueError:
                print("Hibás dátumformátum! Kérjük használja az ÉÉÉÉ.HH.NN formátumot.")
                continue
            eredmeny = foglalas_kezelo.lemondas(szobaszam, datum)
            print(eredmeny)

        elif valasztas == "3":
            print(foglalas_kezelo.foglalasok_listazasa())

        elif valasztas == "4":
            print("Kilépett a szobafoglaló rendszerből. Viszontlátásra!")
            break
        else:
            print("Kérjük, a megadott lehetőségek (1-4) közül válasszon.")

Szobafoglalas()
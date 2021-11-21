from pyswip import Prolog

prolog = Prolog()
prolog.consult("vacatio.pl") # TODO spróbować rozbić na dwa pliki, z samymi ofertami i z API

offer_query = 'not(odrzucona(Id)), oferta(Id, Od, Do, lokalizacja(X), cena(C), T), klimat(lokalizacja(X), srodziemnomorski), cenowo(cena(C), budzetowa), morsko(T).'
# TODO 1 - klasa do składania dynamicznie kryteriów do ofert np. dokładanie morsko na podstawie pytania
to_not_accept = None

# Sprawdzamy ile spełniło
print(len(list(prolog.query(offer_query))))

# Jeśli odpowiednio mało to podajemy i pytamy czy akceptowana czy odrzucana
for offer in prolog.query(offer_query):
    print(offer["Id"], "is the ofert from", offer["Od"], " to ", offer["Do"], " in ", offer["X"])
    to_not_accept = offer["Id"]

# Jak odrzucana to zapisujemy w bazie wiedzy
prolog.query("odrzuc(" + to_not_accept + ").") # ?
prolog.assertz("xodrzucona(" + to_not_accept + ")")

# Pytamy o kolejna
for new_offer in prolog.query(offer_query):
    print(new_offer["Id"], "is the ofert from", new_offer["Od"], " to ", new_offer["Do"], " in ", new_offer["X"])

# TODO 2 - pętla pytająca i uzywające składania dynamicznego do sprawdzania ofert. Jak wszystkie odrzucone to zaczynamy całość od nowa.
# Założenie, pytania zadajemy losowo
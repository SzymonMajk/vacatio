from pyswip import Prolog

class DynamicQuery():
    def __init__(self):
        self.raw_query = "not(odrzucona(Id)), oferta(Id, Od, Do, lokalizacja(X), cena(C), T),"
        self.climate = ""
        self.price = ""
        self.customs = []
    
    def set_climate(self, climate_name):
        self.climate = "klimat(lokalizacja(X), " + climate_name + "),"
    
    def set_price(self, price_name):
        self.price = "cenowo(cena(C), " + price_name + ")"
    
    def set_from(self, date_from):
        pass
    
    def set_to(self, date_to):
        pass

    def append_custom(self, predicate_name):
        self.customs.append(", " + predicate_name + "(T)")

    def render(self):
        customs = ""

        for custom in self.customs:
            customs += custom
        
        return self.raw_query + self.climate + self.price + customs + "."

prolog = Prolog()
prolog.consult("vacatio_core.pl")
prolog.consult("vacatio_offers.pl")

# TODO - pętla pytająca i uzywające składania dynamicznego do sprawdzania ofert. Jak wszystkie odrzucone to zaczynamy całość od nowa.
# Założenie, pytania zadajemy losowo

query = DynamicQuery()
query.set_climate("umiarkowany")
query.set_price("tania")
query.append_custom("wiejsko")
offer_query = query.render()

print(offer_query)

for offer in prolog.query(offer_query):
    print(offer["Id"], "is the ofert from", offer["Od"], " to ", offer["Do"], " in ", offer["X"])

query = DynamicQuery()
query.set_climate("srodziemnomorski")
query.set_price("budzetowa")
query.append_custom("morsko")
offer_query = query.render()
to_not_accept = None

# Sprawdzamy ile spełniło
print(len(list(prolog.query(offer_query))))

print(offer_query)

# Jeśli odpowiednio mało to podajemy i pytamy czy akceptowana czy odrzucana
for offer in prolog.query(offer_query):
    print(offer["Id"], "is the ofert from", offer["Od"], " to ", offer["Do"], " in ", offer["X"])
    to_not_accept = offer["Id"]

# Jak odrzucana to zapisujemy w bazie wiedzy
prolog.query("odrzuc(" + to_not_accept + ").") # ?
print("xodrzucona(" + to_not_accept + ")")
prolog.assertz("xodrzucona(" + to_not_accept + ")")

# Pytamy o kolejna
for new_offer in prolog.query(offer_query):
    print(new_offer["Id"], "is the ofert from", new_offer["Od"], " to ", new_offer["Do"], " in ", new_offer["X"])


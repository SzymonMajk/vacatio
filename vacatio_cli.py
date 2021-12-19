from datetime import date
from pyswip import Prolog
from datetime import datetime

class DynamicQuery():
    def __init__(self):
        self.raw_query = "not(odrzucona(Id)), oferta(Id, Od, Do, lokalizacja(X), cena(C), T),"
        self.date_from = ""
        self.date_to = ""
        self.climate = ""
        self.price = ""
        self.customs = []
    
    def set_climate(self, climate_name):
        self.climate = "klimat(lokalizacja(X), " + climate_name + "),"
    
    def set_price(self, price_name):
        self.price = "cenowo(cena(C), " + price_name + ")"
    
    def set_from(self, date_from):
        self.date_from = "przed(Od, '" + date_from.strftime("%Y-%m-%d") + "'),"
    
    def set_to(self, date_to):
        self.date_to = "po(Do, '" + date_to.strftime("%Y-%m-%d") + "'),"

    def append_custom(self, predicate_name):
        self.customs.append(", " + predicate_name + "(T)")

    def render(self):
        customs = ""

        for custom in self.customs:
            customs += custom
        
        return self.raw_query + self.date_from + self.date_to + self.climate + self.price + customs + "."

prolog = Prolog()
prolog.consult("vacatio_core.pl")
prolog.consult("vacatio_offers.pl")

print("Rekomender wakacji:")
climate_list = ['srodziemnomorski', 'gorski', 'umiarkowany']
prices = ['budzetowa', 'tania', 'droga']
location_type = ['morsko', 'gorsko', 'wiejsko', ' miejsko',  'starozytno']
canceled_offers = []
program = True

while program:
    query = DynamicQuery()
    print("Kiedy najwcześniej mógłbyś wyjechać?")
    date_start = input()
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    query.set_from(date_start)
    print("Kiedy najpóźniej mógłbyś wyjechać?")
    date_stop = input()
    date_stop = datetime.strptime(date_stop, '%Y-%m-%d')
    query.set_to(date_stop)

    for climate in climate_list:
        print(f'Czy interesuje cię klimat {climate}?')
        x = input()
        if x == 'y':
            query.set_climate(climate)
            break

    for price in prices:
        print(f'Czy interesuje cię wyjazd, którego cena jest {price}?')
        x = input()
        if x == 'y':
            query.set_price(price)
            break

    for location in location_type:
        print(f'Czy interesuje cię wyjazd w miejsce , gdzie jest  {location}?')
        x = input()
        if x == 'y':
            query.append_custom(location)
            break

    offer_query = query.render()
    print(offer_query)
    for offer in prolog.query(offer_query):
        to_not_accept = offer["Id"]
        if to_not_accept not in canceled_offers:
            print("Proponowana wycieczka:")
            print(offer["Id"], "is the ofert from", offer["Od"], " to ", offer["Do"], " in ", offer["X"])
            print("Czy ją akceptujesz?")
            x = input()
            if x == 'y':
                program = False
                print("Gratulujemy udanego wyboru")
                break
            else:
                canceled_offers.append(to_not_accept)

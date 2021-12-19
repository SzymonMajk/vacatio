from datetime import date
from pyswip import Prolog
from datetime import datetime
from tkinter import *
from tkcalendar import Calendar

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

class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.prolog = Prolog()
        self.prolog.consult("vacatio_core.pl")
        self.prolog.consult("vacatio_offers.pl")

        self.climate_list = ['srodziemnomorski', 'gorski', 'umiarkowany']
        self.prices = ['budzetowa', 'tania', 'droga']
        self.location_types = ['morsko', 'gorsko', 'wiejsko', ' miejsko',  'starozytno']
        self.canceled_offers = []
        self.offered = False
        self.to_not_accept_current = None

        # Add Calendars
        self.cal_from = Calendar(root, selectmode = 'day',
                    year = 2022, month = 5,
                    day = 14)

        self.cal_from.pack(pady = 10)

        self.cal_to = Calendar(root, selectmode = 'day',
                year = 2022, month = 5,
                day = 21)

        self.cal_to.pack(pady = 10)

        # Add boxes
        self.selected_climate = StringVar()
        self.selected_climate.set(self.climate_list[0])
        self.climate_drop = OptionMenu(root, self.selected_climate, *self.climate_list)

        self.climate_drop.pack(pady = 10)

        self.selected_price = StringVar()
        self.selected_price.set(self.prices[0])
        self.price_drop = OptionMenu(root, self.selected_price, *self.prices)

        self.price_drop.pack(pady = 10)

        self.selected_location_type = StringVar()
        self.selected_location_type.set(self.location_types[0])
        self.location_type_drop = OptionMenu(root, self.selected_location_type, *self.location_types)

        self.location_type_drop.pack(pady = 10)

        # Add Button and Label
        self.search_offer = Button(root, text = "Dopasuj oferte", command = self.find_offer).pack(pady = 10)
        self.offer_text = Label(root, text="Offer: ")
        self.offer_text.pack(pady = 10)
        self.accept_offer = Button(root, text = "Wybierz", command = self.accept).pack(pady = 10)
        self.decline_offer = Button(root, text = "Odrzuć", command = self.decline).pack(pady = 10)

    def accept(self):
        if self.offered:
            print("Gratulujemy udanego wyboru")
            root.destroy()

    def decline(self):
        if self.offered:
            self.canceled_offers.append(self.to_not_accept_current)
            self.offered = False
            self.offer_text.config(text = "Offer: ")

    def find_offer(self):
        if not self.offered:
            query = DynamicQuery()
            query.set_from(datetime.strptime(self.cal_from.get_date(), '%m/%d/%y'))
            query.set_to(datetime.strptime(self.cal_to.get_date(), '%m/%d/%y'))
            query.set_climate(self.selected_climate.get())
            query.set_price(self.selected_price.get())
            query.append_custom(self.selected_location_type.get())

            offer_query = query.render()

            print(offer_query)
            for offer in self.prolog.query(offer_query):
                to_not_accept = offer["Id"]
                if to_not_accept not in self.canceled_offers:
                    self.offered = True
                    self.to_not_accept_current = to_not_accept
                    self.offer_text.config(text = "Offer: " + offer["Id"] + " is the offer from " +  offer["Od"] + " to " +  offer["Do"] + " in " + offer["X"])


# Execute Tkinter
root = Tk()
root.geometry("600x750")
app = App(root)
root.mainloop()
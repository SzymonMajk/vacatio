from datetime import date
from pyswip import Prolog
from datetime import datetime
from tkinter import *
from tkcalendar import Calendar
from smile_license import pysmile_license
import pysmile

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
        self.location_types = ['weekendowa', 'tygodniowa', 'dwutygodniowa']
        self.threshold_list=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        self.canceled_offers = []
        self.offered = False
        self.to_not_accept_current = None

        self.quit_btn = Button(root, text="Wyjdź", command=self.quit).pack(pady=5)

        self.selected_threshold = StringVar()
        self.selected_threshold.set(self.threshold_list[0])
        self.threshold_drop = OptionMenu(root, self.selected_threshold, *self.threshold_list)
        self.threshold_drop.pack(pady=5)

        self.selected_climate = StringVar()
        self.selected_climate.set(self.climate_list[0])
        self.climate_drop = OptionMenu(root, self.selected_climate, *self.climate_list)

        self.climate_drop.pack(pady=5)

        self.selected_price = StringVar()
        self.selected_price.set(self.prices[0])
        self.price_drop = OptionMenu(root, self.selected_price, *self.prices)

        self.price_drop.pack(pady=5)

        self.selected_location_type = StringVar()
        self.selected_location_type.set(self.location_types[0])
        self.location_type_drop = OptionMenu(root, self.selected_location_type, *self.location_types)

        self.location_type_drop.pack(pady=5)

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        c1 = Checkbutton(root, text='Morze', variable=self.var1, onvalue=1, offvalue=0)
        c2 = Checkbutton(root, text='Wyspa', variable=self.var2, onvalue=1, offvalue=0)
        c3 = Checkbutton(root, text='Szlaki', variable=self.var3, onvalue=1, offvalue=0)
        c4 = Checkbutton(root, text='Swiatynie', variable=self.var4, onvalue=1, offvalue=0)
        c5 = Checkbutton(root, text='Swieze Powietrze', variable=self.var5, onvalue=1, offvalue=0)
        c1.pack()
        c2.pack()
        c3.pack()
        c4.pack()
        c5.pack()
        self.search_offer = Button(root, text="Dopasuj oferte", command=self.find_offer)
        self.search_offer.pack(pady=5)
        self.offer_text = Label(root, text="Offer: ",height=11, width=35)
        self.offer_text.pack(pady=5)
        self.accept_offer = Button(root, text="Wybierz", command=self.accept)
        self.decline_offer = Button(root, text="Odrzuć", command=self.decline)

        self.net = pysmile.Network()

        # load the network created by Tutorial1

        self.net.read_file("BayesVacatio.xdsl")

        print("Posteriors with no evidence set:")

        self.net.update_beliefs()
        self.print_all_offers(self.net)
    def quit(self):
        root.destroy()

    def accept(self):
        if self.offered:
            self.cal_from.pack_forget()
            self.cal_to.pack_forget()
            self.climate_drop.pack_forget()
            self.price_drop.pack_forget()
            self.location_type_drop.pack_forget()
            self.search_offer.pack_forget()
            self.accept_offer.pack_forget()
            self.decline_offer.pack_forget()
            self.offer_text.config(text="Gratulujemy udanego wyboru")

    def decline(self):
        if self.offered:
            self.canceled_offers.append(self.to_not_accept_current)
            self.offered = False
            self.offer_text.config(text="Offer: ")

            self.accept_offer.pack_forget()
            self.decline_offer.pack_forget()

    def find_offer(self):
        if not self.offered:
            self.threshold = float(self.selected_threshold.get())
            self.change_evidence_and_update(self.net, "Pytanie_o_klimat_2", self.selected_climate.get())
            self.change_evidence_and_update(self.net, "Pytanie_o_cene", self.selected_price.get())
            self.change_evidence_and_update(self.net, "Pytaine_o_dlugosc_wycieczki", self.selected_location_type.get())
            if self.var1.get()==1:
                self.change_evidence_and_update(self.net, "morze", "Tak")
            if self.var2.get()==1:
                self.change_evidence_and_update(self.net, "wyspa", "Tak")
            if self.var3.get()==1:
                self.change_evidence_and_update(self.net, "szlaki2", "Tak")
            if self.var4.get()==1:
                self.change_evidence_and_update(self.net, "swiatynie", "Tak")
            if self.var5.get()==1:
                self.change_evidence_and_update(self.net, "swieze_powietrze", "Tak")
            self.net.update_beliefs()
            offer = self.return_offers(self.net)
            self.offer_text.config(text=offer)

            # query = DynamicQuery()
            # query.set_from(datetime.strptime(self.cal_from.get_date(), '%m/%d/%y'))
            # query.set_to(datetime.strptime(self.cal_to.get_date(), '%m/%d/%y'))
            # query.set_climate(self.selected_climate.get())
            # query.set_price(self.selected_price.get())
            # query.append_custom(self.selected_location_type.get())
            #
            # offer_query = query.render()
            #
            # print(offer_query)
            # for offer in self.prolog.query(offer_query):
            #     to_not_accept = offer["Id"]
            #     if to_not_accept not in self.canceled_offers:
            #         self.accept_offer.pack(padx=50, side=LEFT)
            #         self.decline_offer.pack(padx=50, side=RIGHT)
            #
            #         self.offered = True
            #         self.to_not_accept_current = to_not_accept
            #         self.offer_text.config(
            #             text="Offer: " + offer["Id"] + " is the offer from " + offer["Od"] + " to " + offer[
            #                 "Do"] + " in " + offer["X"])


    def print_all_offers(self, net):
        d= net.get_all_nodes()
        for handle in net.get_all_nodes():
            if handle in [11, 12, 13, 14, 15]:
                self.print_posteriors(net, handle)

    def print_posteriors(self, net, node_handle):

        node_id = net.get_node_id(node_handle)

        if net.is_evidence(node_handle):

            print(node_id + " has evidence set (" +

                  net.get_outcome_id(node_handle,

                                     net.get_evidence(node_handle)) + ")")

        else:

            posteriors = net.get_node_value(node_handle)

            for i in range(0, len(posteriors)):
                print("P(" + node_id + "=" +

                      net.get_outcome_id(node_handle, i) +

                      ")=" + str(posteriors[i]))

    def return_offers(self, net):
        d = net.get_all_nodes()
        list_offers=[]
        for node_handle in net.get_all_nodes():
            if node_handle in [11, 12, 13, 14, 15]:
                node_id = net.get_node_id(node_handle)

                if net.is_evidence(node_handle):

                    print(node_id + " has evidence set (" +

                          net.get_outcome_id(node_handle,

                                             net.get_evidence(node_handle)) + ")")

                else:

                    posteriors = net.get_node_value(node_handle)

                    for i in range(0, len(posteriors)):
                        #print("P(" + node_id + "=" + net.get_outcome_id(node_handle, i) + ")=" + str(posteriors[i]))
                        if posteriors[i] >= self.threshold and net.get_outcome_id(node_handle, i) == "take":
                            list_offers.append("P(" + node_id + "=" + net.get_outcome_id(node_handle, i) + ")=" + str(round(posteriors[i], 3))+"\n")
        return list_offers
    def print_all_posteriors(self, net):

        for handle in net.get_all_nodes():
            self.print_posteriors(net, handle)

    def change_evidence_and_update(self, net, node_id, outcome_id):

        if outcome_id is not None:

            net.set_evidence(node_id, outcome_id)

        else:

            net.clear_evidence(node_id)

        net.update_beliefs()

        self.print_all_offers(net) # changed from print all posteriors

        print("")

# Execute Tkinter
root = Tk()
root.geometry("400x650")
app = App(root)
root.mainloop()
import pysmile

from smile_license import pysmile_license


# Tutorial2 loads the XDSL file created by Tutorial1,

# then performs the series of inference calls,

# changing evidence each time.


class Tutorial2:

    def __init__(self):

        print("Starting Tutorial2...")

        net = pysmile.Network()

        # load the network created by Tutorial1

        net.read_file("BayesVacatio.xdsl")

        print("Posteriors with no evidence set:")

        net.update_beliefs()

        #self.print_all_posteriors(net)

        print("Setting Pytanie o klimat.")
        self.change_evidence_and_update(net, "Pytanie_o_klimat_2", "umiarkowany")
        print("######################################################")

        self.change_evidence_and_update(net, "Pytanie_o_klimat_2", "gorski")
        print("######################################################")


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

t =Tutorial2()


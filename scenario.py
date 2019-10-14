""" 
    Define a scenario
"""

# ===============================================================================
# Imports
# ===============================================================================

import numpy as np

from network import TrafficNetwork
from demand import TrafficDemand, Demand

from carfollow import K_X, W_I, U_I
from carfollow import Tampere

# ===============================================================================
# Constants
# ===============================================================================

C = U_I * W_I * K_X / (U_I + W_I) * 3600  # veh /h
T_SIM = 720
MPR = 0.5

np.random.seed(42)  # Reproducibility MPR

# Initializing vehicles
Tampere.reset()

# ===============================================================================
# Defaults
# ===============================================================================

test_case = TrafficNetwork((20000, 10000), (1, 2))
demands = Demand((C / 2,), (12,))
trf_dmd = {"lks": (1,), "demands": (demands, demands)}

traffic_demand = TrafficDemand(**trf_dmd)


# ===============================================================================
# Classes
# ===============================================================================


class Scenario:
    def __init__(self, t_network=test_case, traffic_demand=traffic_demand, mpr=MPR):
        self.network = t_network
        self.demand = traffic_demand
        self.mpr = mpr

    def link_demand_network(self):
        """ This will register cars within the traffic network"""

        # create vehicles
        for lk in self.network:
            dmd = self.demand[lk]
            if dmd:
                N_veh = len(dmd)
                v_class_lk = self.get_vehicle_class_per_link(N_veh)
                x_0 = self.demand[lk].full_positions
                v_0 = np.ones(N_veh) * U_I
                self.generate_vehicle_list(x_0, v_0,v_class_lk)

    def get_vehicle_class_per_link(self, N):
        """ Generaate vehicles """
        id_cav = np.random.randint(Tampere.lid, Tampere.lid + N - 1, int(N * self.mpr))  # Id Connected Vehicles
        d_class = {k: "CAV" for k in id_cav}
        v_class = [d_class.get(i, "HDV") for i in range(N)]  # All vehicle types
        return v_class

    def generate_vehicle_list(self, x_0, v_0, v_class):
        """
            Generate veh_list 
        """

        
        for x0, v0, vtype in zip(x_0, v_0, v_class):
            self.veh_list.append(Tampere(x0, v0, vtype))

        # Setting leader for vehicle i
        for i in range(1, N):
            veh_list[i].set_leader(veh_list[i - 1])

    # for lk in self.network:

    #     ID_CAV = np.random.randint(1, N - 1, int(N * MPR))  # Id Connected Vehicles

    # # ID_CAV = (2,)
    # D_CLASS = {k: "CAV" for k in ID_CAV}
    # V_CLASS = [D_CLASS.get(i, "HDV") for i in range(N)]  # All vehicle types
    # T_ACCEPT = SHIFT_CONG - np.random.exponential(PERCEP_RADIOUS, N * 1000)
    # T_ACCEPT = T_ACCEPT[(T_ACCEPT > 0) & (T_ACCEPT < SHIFT_CONG)]
    # T_ACCEPT = np.random.choice(T_ACCEPT, N)


x = Scenario()
x.link_demand_network()

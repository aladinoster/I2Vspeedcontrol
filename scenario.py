""" 
    Define a scenario
"""

# ==============================================================================
# Imports
# ==============================================================================

import numpy as np

from network import TrafficNetwork
from demand import TrafficDemand, Demand

from carfollow import K_X, W_I, U_I
from carfollow import Tampere

# ==============================================================================
# Constants
# ==============================================================================

C = U_I * W_I * K_X / (U_I + W_I) * 3600  # veh /h
T_SIM = 720
MPR = 0.5

np.random.seed(42)  # Reproducibility MPR

# Initializing vehicles
Tampere.reset()

# ==============================================================================
# Defaults
# ==============================================================================

# Traffic Network
trf_net = {"lengths_per_link": (20000, 10000), "lanes_per_link": (1, 2)}
traffic_network = TrafficNetwork(**trf_net)


# Demand
demands = Demand((C / 2,), (12,))
trf_dmd = {"lks": (1,), "demands": (demands, demands)}

traffic_demand = TrafficDemand(**trf_dmd)


# ==============================================================================
# Classes
# ==============================================================================


class Scenario:
    def __init__(
        self,
        traffic_network=traffic_network,
        traffic_demand=traffic_demand,
        mpr=MPR,
    ):
        self.network = traffic_network
        self.demand = traffic_demand
        self.mpr = mpr
        self.link_demand_network()

    def link_demand_network(self):
        """ This will register cars within the traffic network"""

        # create vehicles
        for lk in self.network.link_order:
            dmd = self.demand[lk]
            if dmd:
                N_veh = len(dmd)
                V_class = self.get_vehicle_class_per_link(N_veh)
                X_0 = np.flip(self.demand[lk].full_positions)
                V_0 = np.ones(N_veh) * U_I
                veh_0 = self.get_ic_vehicles_per_lane(X_0, V_0, V_class, lk)
                self.generate_vehicle_list(veh_0, lk)

    def get_vehicle_class_per_link(self, N):
        """ Generaate vehicles """
        id_cav = np.random.randint(
            Tampere.lid, Tampere.lid + N - 1, int(N * self.mpr)
        )  # Id Connected Vehicles
        d_class = {k: "CAV" for k in id_cav}
        v_class = tuple(
            d_class.get(i, "HDV") for i in range(N)
        )  # All vehicle types
        return v_class

    def get_ic_vehicles_per_lane(
        self, X_0: np.array, V_0: np.array, V_class: tuple, link: int
    ):
        """ Retrieve intial condition vehicle state per lane"""
        n_lanes = len(self.network[link])
        veh_0 = {}
        for i, ln in enumerate(self.network[link]):
            veh_0[ln] = (X_0[i::n_lanes], V_0[i::n_lanes], V_class[i::n_lanes])
        return veh_0

    def generate_vehicle_list(self, veh_0: dict, link: int):
        """
            Generate veh_list 
        """
        # Iterate over all lanes
        for ln in self.network[link].lane_order:

            # Iterate over all vehicles
            for x, v, vtype in zip(*veh_0[ln]):
                self.network[link][ln].veh_list.append(
                    Tampere(x0=x, v0=v, l0=ln, veh_type=vtype)
                )

            N_veh_lane = len(self.network[link][ln].veh_list)

            # Setting leader for vehicle i
            for i in range(1, N_veh_lane):
                self.network[link][ln].veh_list[i].set_leader(
                    self.network[link][ln].veh_list[i - 1]
                )

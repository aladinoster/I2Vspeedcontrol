""" 
    Simluation control 
"""

# ===============================================================================
# Imports
# ===============================================================================

from network import TrafficNetwork

from typing import Iterator

# ===============================================================================
# Constants
# ===============================================================================

T_TOTAL = 720  # Simulation time

# ===============================================================================
# Classes
# ===============================================================================


class SimulationControl:
    """  Simulation control
    """

    def __init__(self, traffic_network, time_total):
        self.tfnet = traffic_network
        self.time_iterator = time_total

    def set_demand(self, demand):
        self._dmd = demand

    @property
    def t_s(self) -> int:
        """ Current time step"""
        return next(self._tsim)

    @property
    def time_iterator(self) -> Iterator[int]:
        """ Iterator in"""
        return self._tsim

    @time_iterator.setter
    def time_iterator(self, value=T_TOTAL) -> None:
        self._tsim = range(T_TOTAL)

    def solve_merges(self) -> None:
        """ Solve potential merges for a network """

    def run_simulation(self) -> None:
        """ Execute a traffic simulator"""
        for t in self.time_iterator:
            # self.solve_merges() # 1 link at a time
            for link in self.tfnet:
                link.evolve_step()

        # for t, u in zip(time, lead_acc):
        #     for veh in veh_list:
        #         if veh.type == "CAV" and not veh.acc:
        #             t_accept = T_ACCEPT[veh.idx]
        #             # t_accept = 100
        #             if t >= t_accept:
        #                 acc = U_I + speed_change(time, SPEED_REDUCTION, SHIFT_CONG - t)
        #                 veh.register_control_speed(acc)
        #         veh.step_evolution(control=u)

    # for lk in self.network:

    #     ID_CAV = np.random.randint(1, N - 1, int(N * MPR))  # Id Connected Vehicles

    # # ID_CAV = (2,)
    # D_CLASS = {k: "CAV" for k in ID_CAV}
    # V_CLASS = [D_CLASS.get(i, "HDV") for i in range(N)]  # All vehicle types
    # T_ACCEPT = SHIFT_CONG - np.random.exponential(PERCEP_RADIOUS, N * 1000)
    # T_ACCEPT = T_ACCEPT[(T_ACCEPT > 0) & (T_ACCEPT < SHIFT_CONG)]
    # T_ACCEPT = np.random.choice(T_ACCEPT, N)

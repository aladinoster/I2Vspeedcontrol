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
        self.time_iterator = T_TOTAL 

    def set_demand(self, demand):
        self._dmd = demand

    @property
    def t_s(self)->int:
        """ Current time step"""
        return next(self._tsim)
    
    @property
    def time_iterator(self)-> Iterator[int]:
        """ Iterator in"""
        return self._tsim

    @time_iterator.setter
    def time_iterator(self, value=T_TOTAL)->None:
        self._tsim = iter(range(T_TOTAL))

    def run_simulation(self):
        """ Execute a traffic simulator"""
        for i in time_iterator
        self.
        for link in self.tfnet:
            .solve_merges()


        # for t, u in zip(time, lead_acc):
        #     for veh in veh_list:
        #         if veh.type == "CAV" and not veh.acc:
        #             t_accept = T_ACCEPT[veh.idx]
        #             # t_accept = 100
        #             if t >= t_accept:
        #                 acc = U_I + speed_change(time, SPEED_REDUCTION, SHIFT_CONG - t)
        #                 veh.register_control_speed(acc)
        #         veh.step_evolution(control=u)

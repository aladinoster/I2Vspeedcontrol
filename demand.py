""" 
    Demand Generator
"""


# ===============================================================================
# Imports
# ===============================================================================

import collections.abc

import numpy as np

from plottools import plot_histogram, plot_stairs
from bokeh.plotting import show
from bokeh.layouts import row, column

from carfollow import K_X, W_I, U_I

# ===============================================================================
# Constants
# ===============================================================================

C = U_I * W_I * K_X / (U_I + W_I) * 3600  # veh /h

np.random.seed(35)  # Reproducibility Flow

# ===============================================================================
# Classes
# ===============================================================================


class Demand:
    """ Demand for a single link not lane"""

    def __init__(self, flow_values_vh=(C,), flow_duration_m=(1,), sim_time: int = 12):
        self.value_duration = dict(zip(flow_values_vh, flow_duration_m))
        self.create_demand_pattern()
        self.sim_time = sim_time

    def find_times_exponential(self, flow_vh: float = 60, time_min: int = 1) -> np.array:
        """ Find the times of emission of x vehicles """
        flow_vm = np.clip(flow_vh / 60, 1, C / 60)  # vehicles per minute (value given in veh/h)
        n_vehicles = int(flow_vm * time_min)
        arrival_rate = 3600 / flow_vh  # s / veh
        self.time_headways = np.random.exponential(arrival_rate, n_vehicles)
        return self.time_headways

    def compute_headwayspace(self, flow_vh, time_min) -> np.array:
        """ Find headway space from a time gap"""
        self.space_headways = self.find_times_exponential(flow_vh, time_min) * U_I
        return self.space_headways

    def compute_x0(self, flow_vh, time_min) -> np.array:
        """ Find intial positions for vehicles"""
        return np.cumsum(self.compute_headwayspace(flow_vh, time_min))

    def create_demand_pattern(self):
        full_positions = np.array([0])
        for flow, duration in self.value_duration.items():
            new_spacings = full_positions[-1] + self.compute_x0(flow, duration)
            full_positions = np.concatenate((full_positions, new_spacings))
        self.full_positions = full_positions

    def plot_demand_elements(self) -> None:
        """ A plot to illustrate the demand behavior created 
        """
        space_hwy = plot_histogram(self.space_headways, "Spacing [m]")
        time_hwy = plot_histogram(self.time_headways, "Time Gap [s]")
        time_sim = [0] + list(self.value_duration.values())
        time_cum = np.cumsum(time_sim)
        avg_flow = list(self.value_duration.keys())
        avg_flow = [avg_flow[0]] + avg_flow
        step_flow = plot_stairs(time_cum, avg_flow, "Input Flow", "Time [min]", "Flow [veh/h]")
        return row(space_hwy, time_hwy, step_flow)

    def __len__(self) -> int:
        """ Number of cars"""
        return len(self.full_positions)

    def __repr__(self):
        return f"{self.__class__.__name__}({tuple(self.value_duration.keys())},{tuple(self.value_duration.values())})"

    def __str__(self):
        return str(self.value_duration)


class TrafficDemand(collections.abc.MutableMapping):
    """ Demand for a traffic network"""

    def __init__(self, lks: tuple = (0,), demands: tuple = Demand()):
        self.__dct = dict(zip(lks, demands))

    def __getitem__(self, item):
        return self.__dct.get(item, None)

    def __setitem__(self, key, item):
        self.__dct[key] = item

    def __delitem__(self, key):
        del self.__dct[key]

    def __iter__(self):
        self.dctit = iter(self.__dct.items())
        return self.dctit

    def __next__(self):
        return next(self.dctit)

    def __len__(self):
        return len(self.__dct)

    def __str__(self):
        return str(self.__dct)

    def __repr__(self):
        return f"{self.__class__.__name__}({tuple(self.__dct.keys())},{tuple(self.__dct.values())})"

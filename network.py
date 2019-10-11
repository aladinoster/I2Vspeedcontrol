"""
    Network Traffic + V2V 
"""

# ===============================================================================
# Imports
# ===============================================================================

from itertools import count, repeat
from collections import deque

import networkx as nx


# ===============================================================================
# Constants
# ===============================================================================
L_MAX = 20000

# ===============================================================================
# Classes
# ===============================================================================


class TrafficLane:

    __idx = count(0)  # Vehicle ID

    __slots__ = ["length", "veh_list", "idx"]

    def __init__(self, length: float = L_MAX) -> None:
        self.idx = next(self.__class__.__idx)
        self.length = length
        self.veh_list = deque([])

    def attach_vehicle(self, vehicle) -> None:
        """ Attach a vehicle a vehicle to a lane"""
        self.veh_list.append(vehicle)
        vehicle.veh_leader.set_leader(self.veh_list[-1])

    def detach_vehicle(self) -> None:
        """ Detach head vehicle a vehicle from the  lane"""
        self.veh_list[1].control = self.veh_list[0].control
        self.veh_list.pop()


class TrafficLink:

    __slots__ = ["_lanes", "__lro", "idx"]
    __idx = count(0)  # Vehicle ID

    def __init__(self, length: float = L_MAX, n_lanes: int = 1) -> None:
        self.idx = next(self.__class__.__idx)
        self._lanes = tuple(TrafficLane(length) for n in range(n_lanes))
        self.__lro = set(lk.idx for lk in self._lanes)

    @property
    def lane_order(self):
        """ Link resolution order"""
        return self.__lro

    @lane_order.setter
    def lane_order(self, lro):
        """ lro stands for link resolution order"""
        self.__lro = lro

    def __iter__(self):
        """Iter protocol"""
        return iter(self.lane_order)

    def __next__(self):
        yield next(self.lane_order)


class TrafficNetwork:

    __slots__ = ["_links", "__lro", "idx"]
    __idx = count(0)  # Vehicle ID

    def __init__(self, lengthslinks: list = [L_MAX], laneslinks: list = [1]) -> None:
        self.idx = next(self.__class__.__idx)
        self._links = tuple(
            TrafficLink(length, lanes) for length, lanes in zip(lengthslinks, laneslinks)
        )
        self.__lro = (lk.idx for lk in self._links)

    def set_physical_connection(self, matrix_linkid):
        pass

    @property
    def link_order(self):
        """ Link resolution order"""
        return self.__lro

    @link_order.setter
    def link_order(self, lro):
        """ lro stands for link resolution order"""
        self.__lro = lro

    def __iter__(self):
        """Iter protocol"""
        return self.link_order

    def __next__(self):
        yield next(self.link_order)


class ScenarioCase(TrafficNetwork):
    """ Fills specific for a particular traffic network"""

    def __init__(self):
        pass

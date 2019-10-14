"""
    Network Traffic + V2V 
"""

# ===============================================================================
# Imports
# ===============================================================================

from itertools import count, repeat
from collections import deque, abc

import networkx as nx


# ===============================================================================
# Constants
# ===============================================================================
L_MAX = 20000

# ===============================================================================
# Classes
# ===============================================================================


class TrafficLane:

    __idx = count(0)  # Lane ID

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

    __slots__ = ["__lanes", "__lro", "idx"]
    __idx = count(0)  # Link ID

    def __init__(self, length: float = L_MAX, n_lanes: int = 1) -> None:
        self.idx = next(self.__class__.__idx)
        self.__lanes = tuple(TrafficLane(length) for n in range(n_lanes))
        self.__lro = tuple(ln.idx for ln in self.__lanes)

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
        """Iter protocol"""
        yield next(self.lane_order)

    def __len__(self):
        """ Amount of lanes in link """
        return len(self.__lanes)


class TrafficNetwork(abc.MutableMapping):

    __slots__ = ["__links", "__lro", "idx", "__iter_links"]
    __idx = count(0)  # Network ID

    def __init__(self, lengths_per_link: tuple = (L_MAX,), lanes_per_link: tuple = (1,)) -> None:
        self.idx = next(self.__class__.__idx)
        tuple_link = tuple(
            TrafficLink(length, lanes) for length, lanes in zip(lengths_per_link, lanes_per_link)
        )
        self.__links = {x.idx: x for x in tuple_link}
        self.__lro = {lk.idx: lk.lane_order for lk in self.__links.values()}

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
        self.__iter_links = iter(self.__links)
        return self.__iter_links

    def __next__(self):
        """Iter protocol"""
        return next(self.__iter_links)

    def __getitem__(self, item) -> None:
        """Mapping protocol"""
        return self.__links.get(item, None)

    def __setitem__(self, key, item: TrafficLink) -> None:
        """Mapping protocol"""
        self.__links[key] = item

    def __delitem__(self, key) -> None:
        """Mapping protocol"""
        del self.__links[key]

    def __len__(self):
        """ Amount of links in network"""
        return len(self.__links)

    def __str__(self):
        return str(self.__lro)

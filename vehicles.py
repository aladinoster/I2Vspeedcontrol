""" 
    Vehicle behavior
"""


# ===============================================================================
# Imports
# ===============================================================================

from itertools import count
from typing import Optional

# ===============================================================================
# Constants
# ===============================================================================

U_I = 25
W_I = 6.25  # 5  # 6.25
K_X = 0.16  # 0.2  # 0.16
DT = 1 / (W_I * K_X)

A_MAX = 0.5
A_MIN = -0.5

# ===============================================================================
# Clases
# ===============================================================================


class Vehicle(object):
    """ 
        This data implements the Car Following Law. 
        
        To initialize a vehicle
        
        Vehicle(x0,v0)
        
    """

    _idx = count(0)  # Vehicle ID
    lid = 0

    __slots__ = ["x_t", "v_t", "a_t", "l_t","a", "control", "_veh_lead", "idx", "type"]

    def __init__(
        self, init_pos: float, init_spd: float, lane:float, veh_type: str = "HDV", veh_lead=None
    ) -> None:
        """ 
            Initialization of vehicle state
        """
        # Veh info
        self.idx = next(self.__class__._idx)
        Vehicle.lid = self.idx
        self.type = veh_type
        # Veh state description

        # x: position,
        # x_t: past_position
        # v: speed,
        # v_t: past_speed
        # a: acceleration,
        # a_t: past_acceleration

        self.x_t = init_pos
        self.v_t = init_spd
        self.a_t = 0.0

        self.l_t = lane

        # Control acceleration (leader only)
        self.a = 0.0

        # Vehicle leader definition
        self._veh_lead = veh_lead

        self.control = 0.0

    @classmethod
    def reset(cls) -> None:
        """
            This is a reset vehicle id.
        """
        cls.idx = count(0)

    @property
    def veh_lead(self) -> "Vehicle":
        """
            Retrieve the pointer towards this vehicle's leader
        """
        return self._veh_lead

    def set_leader(self, veh_lead) -> None:
        """
            Set the leader of a vehicle 
        """
        self._veh_lead = veh_lead

    @property
    def v(self) -> float:
        """
            Dynamic equation speed
        """
        return self.v_t + self.a * DT

    @property
    def x(self) -> float:
        """
            Dynamic equation position 
        """
        return self.x_t + self.v * DT  # Check carefully

    # Leader vehicle 2nd order

    def shift_state(self) -> None:
        """
            Shift state
        """
        self.x_t = self.x
        self.v_t = self.v
        self.a_t = self.a

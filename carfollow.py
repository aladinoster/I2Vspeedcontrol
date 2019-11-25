""" 
    Car following model
"""

# ===============================================================================
# Imports
# ==============================================================================

import numpy as np
from math import sqrt
from typing import Union
from vehicles import Vehicle, DT, K_X, W_I, U_I

# ==============================================================================
# Constants
# ==============================================================================

T_E = 0.2
S_0 = 1 / K_X

# TAMPERE MODEL
C_1 = 0.5  # Speed difference coefficient
C_2 = 0.5  # Spacing coefficient
C_3 = 0.5  # Tampere coefficient

# IDM MODEL
A_MAX = 3  # Max accel
A_MIN = -3  # Min accel

B = 1.67  # Max decel
DELTA = 4  # Exponent
V_0 = 25  # 90 / 3.6
S_0IDM = 2

# Random component
np.random.seed(1)
SIGMA_A = 0.05

# ==============================================================================
# Clases
# ==============================================================================


class CarFollowLaw(Vehicle):
    """
        Generic Car Following Behavior
    """

    def __init__(
        self,
        x0: float,
        v0: float,
        l0: float,
        veh_type: str = "HDV",
        veh_lead=None,
        behavior: str = None,
    ) -> None:
        super().__init__(
            init_pos=x0, init_spd=v0, init_lane=l0, veh_type=veh_type, veh_lead=veh_lead
        )
        self.behavior = behavior
        self.acc = False

    @property
    def u(self) -> float:
        """
            Free flow speed
        """
        return U_I

    @property
    def w(self) -> float:
        """
            Shockwave speed
        """
        return W_I

    @property
    def k_x(self) -> float:
        """
            Jam density
        """
        return K_X

    @property
    def s0(self) -> float:
        """
            Minimum spacing
        """
        return 1 / self.k_x

    @property
    def vl(self) -> float:
        """
            Leader speed 
        """
        return self.veh_lead.v_t

    @property
    def dv(self) -> float:
        """ 
            Determine current delta of speed
        """
        if self.veh_lead:
            return self.vl - self.v_t
        return 0

    @property
    def xl(self) -> float:
        """
            Leader position
        """
        return self.veh_lead.x_t

    @property
    def s(self) -> float:
        """
            Determine current spacing (X_n-1 - X_n)
        """
        if self.veh_lead:
            return self.xl - self.x_t
        return 0

    @property
    def T(self) -> float:
        """
            Reaction time
        """
        return DT

    @property
    def vd(self):
        """
            Vehicle desired speed
        """
        try:
            return self._vd(self.x_t)
        except (TypeError, AttributeError):
            return U_I

    @vd.setter
    def vd(self, control):
        self._vd = control

    def register_control_speed(self, control):
        """
            This registers an external control signal into the vehicle behavior
        """
        self.vd = control
        self.acc = True

    def step_evolution(self, control: float = 0) -> None:
        """
            Use this method to a single step in the simulation
        """
        self.shift_state()  # x_{k-1} = x{k} move info from last time step into current
        self.control = control  # Update control
        self.car_following()  # Update acceleration


# ==============================================================================
# Tampere Car Following Model
# ==============================================================================


class Tampere(CarFollowLaw):
    """
        Tampere Car Following Model
    """

    __slots__ = ["_c1", "_c2", "_c3"]

    def __init__(
        self, x0: float, v0: float, l0: float, veh_type: str, veh_lead=None, **kwargs
    ) -> None:
        super().__init__(
            x0=x0,
            v0=v0,
            l0=l0,
            veh_type=veh_type,
            veh_lead=veh_lead,
            behavior=self.__class__.__name__,
            **kwargs
        )
        self.set_parameters(**kwargs)

    @property
    def c1(self) -> float:
        """
            Speed difference coefficient
        """
        return self._c1

    @property
    def c2(self) -> float:
        """
            Spacing coefficient
        """
        return self._c2

    @property
    def c3(self) -> float:
        """        
            Tampere coefficient
        """
        return self._c3

    @c1.setter
    def c1(self, value: float = C_1) -> None:
        self._c1 = value

    @c2.setter
    def c2(self, value: float = C_2) -> None:
        self._c2 = value

    @c3.setter
    def c3(self, value: float = C_3) -> None:
        self._c3 = value

    def set_parameters(self, c1=C_1, c2=C_2, c3=C_3) -> None:
        """
            Set default parameters
        """
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    @property
    def s_d(self) -> float:
        """
            Determine desired spacing  (d + gamma * v )
        """
        return self.s0 + 1 / (self.w * self.k_x) * self.v_t

    def cong_acc(self) -> float:
        """
            Breaking term  c_1 (D V) + c_2 (s - s_d)
        """
        return self.c1 * self.dv + self.c2 * (self.s - self.s_d)

    def free_acc(self) -> float:
        """
            Acceleration term (Tampere) c_3 (v_d - v)
        """
        return self.c3 * (self.vd - self.v_t)

    def acel(self) -> float:
        """
            Acceleration term 
        """
        return min(self.cong_acc(), self.free_acc())

    def car_following(self) -> None:
        """ 
            Acceleration car following 
            
            Note: 
                if leader 
                    min(cong_acc, free_acc) -> Tampere
                else 
                    manual acceleration
        """
        if self.veh_lead:
            self.a = max(
                A_MIN, min(self.acel() + np.random.normal(0, SIGMA_A), A_MAX)
            )  # Car following
        else:
            self.vd = self.control
            self.a = max(A_MIN, min(self.free_acc() / 4, A_MAX))


# ==============================================================================
# IDM Car Following Model
# ==============================================================================


class IDM(CarFollowLaw):
    """
        Intelligent Driver's Model Car Following 
    """

    __slots__ = ["_b", "_delta", "_amax"]

    def __init__(self, x0: float, v0: float, veh_lead=None, **kwargs) -> None:
        super().__init__(x0, v0, veh_lead, self.__class__.__name__)
        self.set_parameters(**kwargs)

    @property
    def a_max(self) -> float:
        """
            Comfortable decceleration
        """
        return self._amax

    @a_max.setter
    def a_max(self, value: float = A_MAX) -> None:
        self._amax = value

    @property
    def b(self) -> float:
        """
            Comfortable decceleration
        """
        return self._b

    @b.setter
    def b(self, value: float = B) -> None:
        self._b = value

    @property
    def delta(self) -> float:
        """
            Acceleration exponent 
        """
        return self._delta

    @delta.setter
    def delta(self, value: float = DELTA) -> None:
        self._delta = value

    @property
    def s0(self):
        """ Minimum distance
        """
        return S_0IDM

    def set_parameters(self, a_max=A_MAX, b=B, delta=DELTA) -> None:
        """
            Set default parameters
        """
        self.a_max = a_max
        self.b = b
        self.delta = delta

    def break_strategy(self) -> float:
        """
            BS: v * dv / (2 (a*b)^(1/2))
        """
        return (self.v_t * self.dv) / (2 * sqrt(self.a_max * self.b))

    def s_d(self) -> float:
        """
            s0 + max(vT+BS)
        """
        return self.s0 + max(0, self.v_t * self.T + self.break_strategy())

    def t1(self, vd: float = V_0) -> float:
        """
            (v/vd)^d
        """
        return (self.v_t / vd) ** self.delta

    def t2(self) -> float:
        """
            (sd(v,dv)/s)^2
        """
        return (self.s_d() / self.s) ** 2

    def acel(self, vd) -> float:
        """
            Vehicle acceleration
        """
        return self.a_max * (1 - self.t1() - self.t2())

    def car_following(self, vd: float) -> None:
        """ 
            Acceleration car following 
            
            Note: 
                if leader 
                    min(cong_acc, free_acc) -> Tampere
                else 
                    manual acceleration
        """
        if self.veh_lead:
            self.a = self.acel(vd)  # Car following
        else:
            self.a = self.control  # Leader vehicle 2nd order

"""
   Sent messages
"""

# ===============================================================================
# Imports
# ===============================================================================

from support import speed_pulse, speed_drop

from carfollow import U_I

# ===============================================================================
# Constants
# ===============================================================================


SPEED_REDUCTION = 5.5  # Amount of speed reduction [m/s]
X_CONGESTION = 15000  # Position of congestion in space [m]

# ===============================================================================
# Clases
# ===============================================================================

# Speed Selection
def msg_spd(x, delay):
    """
        Sent message to specific CAV vehicle
        Initial speed: 25 m/s
        Drop: 7m/s
        Position: 14Km 
        Span: 400m
    """
    return speed_drop(x, v0=U_I, drop=SPEED_REDUCTION, delay=delay)


def msg_pls(x, delay):
    """
        Sent message to specific CAV vehicle (Pulse)
        Initial speed: 25 m/s
        Drop: 7m/s
        Position: 14Km 
        Span: 400m
    """
    return speed_pulse(
        x, v0=U_I, drop=SPEED_REDUCTION, delay=delay, duration=X_CONGESTION - delay + 1500
    )


class Msg1:
    """ Creates a random message 1 for a vehicle"""

    def __init__(self, distance):
        self.distance = distance

    def __call__(self, x):
        return msg_spd(x, self.distance)


class Msg2:
    """ Creates a random message 2 for a vehicle"""

    def __init__(self, distance):
        self.distance = distance

    def __call__(self, x):
        return msg_pls(x, self.distance)

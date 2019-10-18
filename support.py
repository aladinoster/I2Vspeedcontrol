""" 
    Support functionalities 
"""

import numpy as np
from carfollow import U_I

np.random.seed(100)


def sigmoid(x, A: float = 1, a: float = 50, d: int = 250):
    """Sigmoid function"""
    return A * 1 / (1 + np.exp(-(x - d) / a))


def deriv_sigmoid(x, A: float = 1, a: float = 50, d: int = 250):
    """Sigmoid derivative function"""
    return (A / a) * sigmoid(x, 1, a, d) * (1 - sigmoid(x, 1, a, d))


def pulse_sigmoid(x, A: float = 1, d: int = 250, duration: float = 1000):
    """Sigmoid pulse minimum duration 1000 meters"""
    d = max(d, 250)  # Minimum effective delay
    duration = max(duration, 1000)  # Minimum effective duration
    effective_duration = 500 + duration - 1000  # Transforming total duration into effective
    return sigmoid(x, A, d=d) - sigmoid(x, A, d=d + effective_duration)


def deriv_pulse_sigmoid(x, A: float = 1, a: float = 50, d: int = 250, duration: float = 1000):
    """Sigmoid pulse derivative"""
    d = max(d, 250)  # Minimum effective delay
    duration = max(duration, 1000)  # Minimum effective duration
    effective_duration = 500 + duration - 1000  # Transforming total duration into effective
    return 20 * deriv_sigmoid(x=x, A=A, a=a, d=d) - 20 * deriv_sigmoid(
        x=x, A=A, a=a, d=d + effective_duration
    )


def speed_pulse(x, v0=U_I, drop: float = 1, delay: int = 250, duration: float = 1000):
    """ Create a decreasing speed pulse"""
    return v0 - pulse_sigmoid(x=x, A=drop, d=delay, duration=duration)


def acceleration_pulse(x, v0=U_I, drop: float = 1, delay: int = 250, duration: float = 1000):
    """ Create a decreasing acceleration pulse"""
    return -deriv_pulse_sigmoid(x=x, A=drop, d=delay, duration=duration)


def speed_drop(x, v0=U_I, drop: float = 1, delay: int = 250):
    """ Create a decreasing jump on speed"""
    return v0 - sigmoid(x, A=drop, d=delay)

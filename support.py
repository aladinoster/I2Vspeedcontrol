""" 
    Support functionalities 
"""
#%%
import numpy as np
from carfollow import SIGMA_A, U_I

np.random.seed(100)


def gaussian(time, s=1):
    """ Gaussian curve """
    x = (time) / (s / 3)
    # A = 1 / (np.sqrt(2 * np.pi) * s)
    return np.exp(-x ** 2)


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


def speed_drop(x,v0=U_I,drop:float=1,delay:int=250):
    """ Create a decreasing jump on speed"""
    return v0-sigmoid(x,A=drop,d=delay)


def shifter(signal, shift: int = 0):
    """ Circular shift of a signal """
    shift = np.clip(shift, 0, 480)  # Safe shift
    return np.roll(signal, shift)


def leader_congestion_pattern(time, shift: int = 0):
    """ Create congestion pattern """
    lead_acc = -np.sin(2 * np.pi * 1 / 60 * (time)) * np.concatenate(
        (np.ones(30), np.zeros(60), np.ones(30), np.zeros(len(time) - 120))
    )
    lead_acc += np.random.normal(0, 0.05, len(time))
    return shifter(lead_acc, shift)


def speed_change(time, change: float = 1, expander: float = 10, shift: int = 0):
    """ Define control vehicle"""
    vit_control = change * (-1 + gaussian(time, s=expander))
    return shifter(vit_control, shift)


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


def sigmoid(x, A: float = 1, a: float = 1, d: int = 5):
    """Sigmoid function"""
    return A * 1 / (1 + np.exp(-(x - d) / a))


def deriv_sigmoid(x, A: float = 1, a: float = 1, d: int = 5):
    """Sigmoid derivative function"""
    return A * sigmoid(x, 1, a, d) * (1 - sigmoid(x, 1, a, d))


def pulse_sigmoid(x, A: float = 1, d: int = 0, duration: float = 30):
    """Sigmoid pulse"""
    delay = duration - 10
    return sigmoid(x, A, d=d + 5) - sigmoid(x, A, d=delay + d + 5)


def deriv_pulse_sigmoid(x, A: float = 1, d: int = 0, duration: float = 30):
    """Sigmoid pulse derivative"""
    delay = duration - 10
    return deriv_sigmoid(x=x, A=A, d=d + 5) - deriv_sigmoid(x=x, A=A, d=delay + d)


def speed_pulse(x, v0=U_I, drop: float = 1, delay: int = 0, duration: float = 30):
    """ Create a decreasing speed pulse"""
    return v0 - pulse_sigmoid(x=x, A=drop, d=delay, duration=duration)


def acceleration_pulse(x, v0=U_I, drop: float = 1, delay: int = 0, duration: float = 30):
    """ Create a decreasing acceleration pulse"""
    return -deriv_pulse_sigmoid(x=x, A=drop, d=delay, duration=duration)


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


#%%
import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

output_notebook()

x = np.linspace(0, 1000, 5000)
y = speed_pulse(x,25,7,800,50)
p = figure()
p.line(x, y)
show(p)

#%%

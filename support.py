""" Support functionalities 
"""

import numpy as np
from carfollow import SIGMA_A

np.random.seed(100)


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


def speed_change(time, shift: int = 0):
    """ Define control vehicle"""
    vit_control = -(1 / (1 + np.exp(-(time - 50) / 10)))
    return shifter(vit_control, shift)

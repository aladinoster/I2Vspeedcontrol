""" Support functionalities 
"""

import numpy as np


def leader_congestion_pattern(time, shift: int = 0):
    """ Create congestion pattern """
    lead_acc = np.sin(2 * np.pi * 1 / 60 * (time)) * np.concatenate(
        (np.zeros(90), np.ones(30), np.zeros(60), np.ones(30), np.zeros(510))
    )
    shift = np.clip(shift, 0, 510)  # Safe shift
    lead_acc = np.roll(lead_acc, shift)
    return lead_acc

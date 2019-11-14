""" 
    Run sensitivity test 
"""

import papermill as pm
from itertools import product
import pandas as pd
import matplotlib.pyplot as plt


Q = (0.3, 0.5, 0.75, 1)
MIN_DIST = (5000, 7500, 10000)
MPR = (0, 0.1, 0.2, 0.3, 0.4)

cases = product(MPR, MIN_DIST, Q)
list_cases = list(product(MPR, MIN_DIST, Q))


for case in cases:
    mpr, min_dist, q = case
    print(case)
    pm.execute_notebook(
        "general.ipynb", "general.ipynb", parameters=dict(MPR=mpr, MIN_DIST=min_dist, Q_PERC=q)
    )





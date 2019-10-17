""" 
    Run sensitivity test 
"""

import papermill as pm
from itertools import product

Q=(0.5, 1)
MIN_DIST=(5000, 10000)
MPR=(0.1, 0.3, 0.5)

cases = product(Q,MIN_DIST,MPR)

for case in cases:
    mpr, min_dist, q = case
    pm.execute_notebook(
        "results_ppmill.ipynb",
        "Untitled.ipynb",
        parameters=dict(MPR=mpr , MIN_DIST=min_dist, Q=q),
    )

""" 
    Run sensitivity test 
"""

import papermill as pm
from itertools import product
import pandas as pd
import matplotlib.pyplot as plt

Q = (0.5, 1)
MIN_DIST = (5000, 10000)
MPR = (0.1, 0.2, 0.3)

cases = product(MPR, MIN_DIST, Q)

for case in cases:
    mpr, min_dist, q = case
    pm.execute_notebook(
        "general.ipynb",
        "general.ipynb",
        parameters=dict(MPR=mpr, MIN_DIST=min_dist, Q_PERC=q),
    )

    
df = pd.read_csv('data/Indicators.csv',names=['mpr','flow','distance','meanTT','stdTT','totalTT'])
df['mpr']=df['mpr']*100

d5000 = df[df['distance'].eq(5000)]
d10000 = df[df['distance'].eq(10000)]

d5000mtt = d5000.pivot(columns='mpr',values='meanTT',index='flow')
d10000mtt = d10000.pivot(columns='mpr',values='meanTT',index='flow')

d5000stt = d5000.pivot(columns='mpr',values='stdTT',index='flow')
d10000stt = d10000.pivot(columns='mpr',values='stdTT',index='flow')

fig,ax = plt.subplots(1,2,figsize=(15,7.5),sharey=True)

ax[0].set_xlabel("Flow [veh/h]")
ax[0].set_ylabel("Travel Time [s]")

ax[1].set_xlabel("Flow [veh/h]")
ax[1].set_ylabel("Travel Time [s]")

d5000mtt.plot(kind='bar',ax=ax[0])
d10000mtt.plot(kind='bar',ax=ax[1])

plt.savefig("data/traveltimemean.png")

fig,ax = plt.subplots(1,2,figsize=(15,7.5),sharey=True)

ax[0].set_xlabel("Flow [veh/h]")
ax[0].set_ylabel("Travel Time [s]")

ax[1].set_xlabel("Flow [veh/h]")
ax[1].set_ylabel("Travel Time [s]")

d5000stt.plot(kind='bar',ax=ax[0])
d10000stt.plot(kind='bar',ax=ax[1])

plt.savefig("data/traveltimestd.png")
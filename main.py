#%%
from carfollow import Tampere, W_I, U_I, K_X
from support import leader_congestion_pattern, speed_change
import numpy as np

#%%
from plotf import plot_single_trace, plot_xva
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.layouts import row, column

# output_notebook()

#%%
# Constants
N = 10  # 50
T_TOTAL = 720  # Simulation time
SHIFT_CONG = 450  # Congestion shift

# Declaring Initial position and initial speed
X0 = np.flip(np.arange(0, N) * (W_I + U_I) / (W_I * K_X))
V0 = np.ones(N) * U_I
A0 = np.zeros(N)

veh_list = []

# Initializing vehicles
Tampere.reset()
for x0, v0 in zip(X0, V0):
    veh_list.append(Tampere(x0, v0))

# Setting leader for vehicle i
for i in range(1, N):
    veh_list[i].set_leader(veh_list[i - 1])


#%%

time = np.arange(T_TOTAL)

# Leader Profile

lead_acc = leader_congestion_pattern(time, shift=SHIFT_CONG)
leader = plot_single_trace(
    time, lead_acc, "Leaders' acceleration", "Time [secs]", "Acceleration [m/s²]"
)

#%%


#%%
# Matrix info storage
X = X0
V = V0
A = A0


for u in lead_acc:
    for veh in veh_list:
        veh.step_evolution(control=u)

    V = np.vstack((V, np.array([veh.v for veh in veh_list])))
    X = np.vstack((X, np.array([veh.x for veh in veh_list])))
    A = np.vstack((A, np.array([veh.a for veh in veh_list])))


#%%
output_file("Summary.html", title="Summary Test")
pos, spd, acc = plot_xva(time, X, V, A)
show(column(row(leader, pos), row(spd, acc)))


#%%

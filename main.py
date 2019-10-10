#%%
from carfollow import Tampere, W_I, U_I, K_X
from support import leader_congestion_pattern, speed_change
import numpy as np

from plotf import plot_single_trace, plot_xva
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.layouts import row, column

# output_notebook()

#%%
# Constants
N = 200  # 50
T_TOTAL = 720  # Simulation time
time = np.arange(T_TOTAL)  # Time vector

SHIFT_CONG = 450  # Congestion shift time appearing
SPEED_REDUCTION = 7  # Amount of speed reduction
PERCEP_RADIOUS = 100

# Scenario conditions
np.random.seed(42)  # Reproducibility
MPR = 0.5  # Market penetration rate
ID_CAV = np.random.randint(1, N - 1, int(N * MPR))  # Id Connected Vehicles
# ID_CAV = (2,)
D_CLASS = {k: "CAV" for k in ID_CAV}
V_CLASS = [D_CLASS.get(i, "HDV") for i in range(N)]  # All vehicle types
T_ACCEPT = SHIFT_CONG - np.random.exponential(PERCEP_RADIOUS, N * 1000)
T_ACCEPT = T_ACCEPT[(T_ACCEPT > 0) & (T_ACCEPT < SHIFT_CONG)]
T_ACCEPT = np.random.choice(T_ACCEPT, N)

# Vehicle Initial position / speed
Q_PERC = 1  # [0,1] Reduces flow, at 1 there's capacity.
X0 = np.flip(np.arange(0, N) * (W_I + U_I) / (W_I * K_X) * Q_PERC)
V0 = np.ones(N) * U_I
A0 = np.zeros(N)

veh_list = []

# Initializing vehicles
Tampere.reset()
for x0, v0, vtype in zip(X0, V0, V_CLASS):
    veh_list.append(Tampere(x0, v0, vtype))

# Setting leader for vehicle i
for i in range(1, N):
    veh_list[i].set_leader(veh_list[i - 1])


#%%
# Leader Profile
lead_acc = leader_congestion_pattern(time, shift=SHIFT_CONG)
leader = plot_single_trace(
    time, lead_acc, "Leaders' acceleration", "Time [secs]", "Acceleration [m/s²]"
)

#%%
# Speed Selection
acc = U_I + speed_change(time, SPEED_REDUCTION, 100)
spd_chg = plot_single_trace(time, acc, "Speed reduction", "Time [secs]", "Speed [m/s]")
show(spd_chg)

#%%
# Matrix info storage
X = X0
V = V0
A = A0


for t, u in zip(time, lead_acc):
    for veh in veh_list:
        if veh.type == "CAV" and not veh.acc:
            t_accept = T_ACCEPT[veh.idx]
            # t_accept = 100
            if t >= t_accept:
                acc = U_I + speed_change(time, SPEED_REDUCTION, SHIFT_CONG - t)
                veh.register_control_speed(acc)
        veh.step_evolution(control=u)

    V = np.vstack((V, np.array([veh.v for veh in veh_list])))
    X = np.vstack((X, np.array([veh.x for veh in veh_list])))
    A = np.vstack((A, np.array([veh.a for veh in veh_list])))


#%%
output_file("Summary.html", title="Summary Test")
pos, spd, acc = plot_xva(time, X, V, A)
show(column(row(leader, pos), row(spd, acc)))


#%%

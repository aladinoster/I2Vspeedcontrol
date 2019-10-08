#%%
from carfollow import IDM, Tampere, W_I, U_I, K_X
import numpy as np

#%%
from plotf import plot_trj
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.layouts import row, column

output_notebook()

#%%
N = 50  # 50

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
time = np.arange(360)

# Sinusoidal signal profile
lead_acc = np.sin(2 * np.pi * 1 / 60 * (time)) * np.concatenate(
    (np.zeros(90), np.ones(60), np.zeros(90), np.zeros(120))
)

leader = figure(title="Leader's acceleration", plot_height=500, plot_width=500)
leader.line(time, lead_acc)


#%%
# Matrix info storage
X = X0
V = V0
A = A0

for u in lead_acc:
    for veh in veh_list:
        veh.step_evolution(v_d=U_I, control=u)

    V = np.vstack((V, np.array([veh.v for veh in veh_list])))
    X = np.vstack((X, np.array([veh.x for veh in veh_list])))
    A = np.vstack((A, np.array([veh.a for veh in veh_list])))

##%%
pos = plot_trj(time, X, V)
spd = plot_trj(time, V, V)
acc = plot_trj(time, A, V)
show(column(row(leader, pos), row(spd, acc)))


#%%

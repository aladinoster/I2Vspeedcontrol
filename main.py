#%%
from carfollow import Tampere, W_I, U_I, K_X, A_MIN, A_MAX
from support import speed_pulse
from messages import Msg1, Msg2
import numpy as np
import pandas as pd

from plottools import plot_single_trace, plot_xva, plot_histogram, plot_multiple_trajectories
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook, export_png
from bokeh.layouts import row, column

# output_notebook()

# Constant values
N = 100  # Number of vehicles to simulate
T_TOTAL = 960  # Simulation time [s]
time = np.arange(T_TOTAL)  # Time vector

# Traffic characteristics
X_CONGESTION = 15000  # Position of congestion in space [m]
L_CONGESTION = 1500  # Approximate congestion length in space [m]

# Messages for V2V
SPEED_REDUCTION = 5.5  # Amount of speed reduction [m/s]
PERCEP_RADIOUS = 3000  # Radious of perception of the broadcasted messages [m]

MPR = 0.1  # Market penetration rate

MIN_DIST = 5000  # Minimum distance for acceptance


#%%
# Capacity
C = (U_I * W_I * K_X) / (W_I + U_I)
# print(f"Capacity value per lane: {C*3600} [veh/h]")

# Vehicle Initial position / speed
Q_PERC = 0.3  # [0,1] Reduces flow, at 1 there's capacity.
TF = C * Q_PERC


#%%
# Vehicle initializer
X0 = np.flip(np.arange(0, N) * (W_I + U_I) / (W_I * K_X) * 1 / Q_PERC)
V0 = np.ones(N) * U_I
A0 = np.zeros(N)

veh_list = []

np.random.seed(42)  # Reproducibility
ID_CAV = np.random.randint(1, N - 1, int(N * MPR))  # Id Connected Vehicles
D_CLASS = {k: "CAV" for k in ID_CAV}
V_CLASS = [D_CLASS.get(i, "HDV") for i in range(N)]  # All vehicle types

# Initializing vehicles
Tampere.reset()
for x0, v0, vtype in zip(X0, V0, V_CLASS):
    veh_list.append(Tampere(x0=x0, v0=v0, l0=0, veh_type=vtype))

# Setting leader for vehicle i
for i in range(1, N):
    veh_list[i].set_leader(veh_list[i - 1])

ID_CAVN = [i for i, j in enumerate(V_CLASS) if j == "CAV"]
# print(ID_CAVN)


#%%
# Scenario conditions
D_ACCEPT = X_CONGESTION - 1000  # Broad casting messages @ 14Km
D_ACCEPT = D_ACCEPT - np.random.exponential(PERCEP_RADIOUS, N * 1000)
D_ACCEPT = D_ACCEPT[(D_ACCEPT > MIN_DIST) & (D_ACCEPT < X_CONGESTION)]
D_ACCEPT = np.random.choice(D_ACCEPT, N)

# msg_hist = plot_histogram(D_ACCEPT, "Message Position [m]")
# show(msg_hist)

#%%
# Road works speed profile
def lead_spd(x):
    """  Leader's function to control speed drop in space 
         Speed Drop: 20 m/s 
         Position: 15 Km
         Duration: 20 Km
    """
    return speed_pulse(x, drop=20, delay=X_CONGESTION, duration=L_CONGESTION)


x_t = np.linspace(0, 20000, 20000)
v_t = lead_spd(x_t)
# leader_xt = plot_single_trace(x_t, v_t, "Leaders' speed", "Space [m]", "Speed [m/s]")
# show(leader_xt)


#%%
# Message definition
# msgfn = Msg1(14000)
# msgtx1 = msgfn(x_t)  # Example of a sent message @ 14Km
# msg_tx1 = plot_single_trace(
#     x_t, msgtx1, "Message 1: Speed reduction", "Position [m]", "Speed [m/s]"
# )

# msgfn = Msg2(14000)
# msgtx2 = msgfn(x_t)  # Example of a sent message @ 14Km
# msg_tx2 = plot_single_trace(
#     x_t, msgtx2, "Message 2: Speed reduction + recovery", "Position [m]", "Speed [m/s]"
# )
# show(row(msg_tx1, msg_tx2))


#%%
# Sent messages
# send_message = Msg2

# tx_message = []

# for veh in veh_list:
#     d_accept = D_ACCEPT[veh.idx]
#     tx_message.append(send_message(d_accept))

# x_ss = np.linspace(0, 20000, 1000)

# acc_values = np.array(list(map(lambda x: x(x_ss), tx_message)))
# acc_values.shape

# p = figure(title="Set of messages transmitted")
# p.xaxis.axis_label = "Position [m]"
# p.yaxis.axis_label = "Speed [m/s]"
# for ac, vc in zip(acc_values, V_CLASS):
#     if vc == "CAV":
#         p.line(x_ss, ac)
# show(p)

#%%
# Dynamical evalution
X = X0
V = V0
A = A0

send_message = Msg2  # Msg2 # Defines the type of message to be send

d_accept = X_CONGESTION - 1000
msg_fix = send_message(d_accept)

for t in time:
    for veh in veh_list:
        if veh.type == "CAV" and not veh.acc:
            d_accept = D_ACCEPT[veh.idx]
            msg = send_message(d_accept)
            veh.register_control_speed(msg)
        elif veh.type == "HDV" and not veh.acc:
            veh.register_control_speed(msg_fix)

        veh.step_evolution(control=lead_spd)

    V = np.vstack((V, np.array([veh.v for veh in veh_list])))
    X = np.vstack((X, np.array([veh.x for veh in veh_list])))
    A = np.vstack((A, np.array([veh.a for veh in veh_list])))

V = V[1:, :]
X = X[1:, :]
A = A[1:, :]

#%%
# Creating plots
x_t = time
v_t = V[:, 0]
leader_vt = plot_single_trace(x_t, v_t, "Leaders' speed", "Time [s]", "Speed [m/s]")
x_t = time
a_t = A[:, 0]
leader_at = plot_single_trace(x_t, a_t, "Leaders' acceleration", "Time [m]", "Acceleration [m/s²]")
zooms = ((MIN_DIST, X_CONGESTION + L_CONGESTION), (-1, U_I + 1), (A_MIN - 0.5, A_MAX + 0.5))
pos, spd, acc = plot_xva(time, X, V, A, y_range=zooms)
poswoz = plot_multiple_trajectories(time, X, V, "Position", "Time [secs]", "Position [m]")
#%%
# Writting leader's file
# filename = "Leader.html"
# output_file(filename)
# show(row(leader_xt, leader_vt, leader_at))

#%%
# Writting trajectories file
data = "data/"
filename = f"pos_mpr-{MPR}_q-{Q_PERC}_d-{MIN_DIST}.png"
export_png(pos, filename=data + filename)
filename = f"poswoz_mpr-{MPR}_q-{Q_PERC}_d-{MIN_DIST}.png"
export_png(poswoz, filename=data + filename)
print(f"File: {filename} has been saved")
filename = f"spd_mpr-{MPR}_q-{Q_PERC}_d-{MIN_DIST}.png"
export_png(spd, filename=data + filename)
print(f"File: {filename} has been saved")
filename = f"acc_mpr-{MPR}_q-{Q_PERC}_d-{MIN_DIST}.png"
export_png(acc, filename=data + filename)
print(f"File: {filename} has been saved")
# show(row(pos, spd, acc))

# line_1 =  Span(location=5000, dimension='width', line_color='orangered',line_dash='dashed', line_width=3)
# line_2 =  Span(location=15000, dimension='width', line_color='orangered',line_dash='dashed', line_width=3)
# line_3 =  Span(location=17900, dimension='width', line_color='orangered',line_dash='dashed', line_width=3)pos.add_layout(line_1)
# pos.add_layout(line_2)
# pos.add_layout(line_3)show(column(row(leader, pos), row(spd, acc)))#%% [markdown]
# # A. Ladino


#%%

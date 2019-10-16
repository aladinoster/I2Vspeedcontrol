#%%
from carfollow import Tampere, W_I, U_I, K_X
from support import speed_change, speed_pulse, speed_drop
import numpy as np

from plottools import plot_single_trace, plot_xva, plot_histogram
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.layouts import row, column

output_notebook()

#%%
# Constants
N = 100  # 50
T_TOTAL = 960  # Simulation time
time = np.arange(T_TOTAL)  # Time vector

# Traffic characteristics
X_CONGESTION = 15000  # Congestion in space
L_CONGESTION = 2000 # Approximate congestion length in space 

# Messages for V2V
SPEED_REDUCTION = 7  # Amount of speed reduction
PERCEP_RADIOUS = 3000

#%%
# Scenario conditions
np.random.seed(42)  # Reproducibility
MPR = 0.5  # Market penetration rate
ID_CAV = np.random.randint(1, N - 1, int(N * MPR))  # Id Connected Vehicles
D_CLASS = {k: "CAV" for k in ID_CAV}
V_CLASS = [D_CLASS.get(i, "HDV") for i in range(N)]  # All vehicle types

D_ACCEPT = X_CONGESTION - 1000 # Broad casting messages @ 14Km
D_ACCEPT = D_ACCEPT - np.random.exponential(PERCEP_RADIOUS, N * 1000)
D_ACCEPT = D_ACCEPT[(D_ACCEPT > 0) & (D_ACCEPT < X_CONGESTION)]
D_ACCEPT = np.random.choice(D_ACCEPT, N)

msg_hist = plot_histogram(D_ACCEPT,"Message Position [m]")
show(msg_hist)

# Vehicle Initial position / speed
Q_PERC = 2  # [0,1] Reduces flow, at 1 there's capacity.
X0 = np.flip(np.arange(0, N) * (W_I + U_I) / (W_I * K_X) * 1/Q_PERC)
V0 = np.ones(N) * U_I
A0 = np.zeros(N)

veh_list = []

# Initializing vehicles
Tampere.reset()
for x0, v0, vtype in zip(X0, V0, V_CLASS):
    veh_list.append(Tampere(x0=x0, v0=v0, l0=0, veh_type=vtype))

# Setting leader for vehicle i
for i in range(1, N):
    veh_list[i].set_leader(veh_list[i - 1])


#%%
# Leader Profile
def lead_spd(x):
    """  Leader's function to control speed drop in space 
         Speed Drop: 20 m/s 
         Position: 15 Km
         Duration: 20 Km
    """
    return speed_pulse(x,drop=20,delay=X_CONGESTION,duration=L_CONGESTION)

x_t = np.linspace(0, 20000, 20000)
v_t = lead_spd(x_t)
leader_xt = plot_single_trace(
     x_t, v_t, "Leaders' speed", "Space [m]", "Speed [m/s]"
)


#%%
# Speed Selection
def msg_spd(x,delay):
    """
        Sent message to specific CAV vehicle
        Initial speed: 25 m/s
        Drop: 7m/s
        Position: 14Km 
        Span: 400m
    """
    return speed_drop(x,v0=U_I, drop=SPEED_REDUCTION, delay=delay)

def msg_pls(x,delay):
    """
        Sent message to specific CAV vehicle (Pulse)
        Initial speed: 25 m/s
        Drop: 7m/s
        Position: 14Km 
        Span: 400m
    """
    return speed_pulse(x,v0=U_I, drop=SPEED_REDUCTION, delay=delay, duration=X_CONGESTION-delay)


acc = msg_spd(x_t,14000) # Example of a sent message @ 14Km
spd_chg = plot_single_trace(x_t, acc, "Speed reduction", "Position [m]", "Speed [m/s]")
show(spd_chg)




class MsgRnd:
    """ Creates a random message for a vehicle"""
    def __init__(self,distance):
        self.distance = distance
    
    def __call__(self,x):
        return self.msg_pls(x,self.distance)

#%%
# Matrix info storage
X = X0
V = V0
A = A0


for t in time:
    for veh in veh_list:
        if veh.type == "CAV" and not veh.acc:
            d_accept = D_ACCEPT[veh.idx]
            msg = MsgRnd(d_accept)
            veh.register_control_speed(msg)
        veh.step_evolution(control=lead_spd)

    V = np.vstack((V, np.array([veh.v for veh in veh_list])))
    X = np.vstack((X, np.array([veh.x for veh in veh_list])))
    A = np.vstack((A, np.array([veh.a for veh in veh_list])))


#%%

x_t = time
v_t = V[:,0]
leader_vt = plot_single_trace(
     x_t, v_t, "Leaders' speed", "Time [s]", "Speed [m/s]"
)
x_t = time
a_t = A[:,0]
leader_at = plot_single_trace(
     x_t, a_t, "Leaders' acceleration", "Time [m]", "Acceleration [m/s²]"
)

show(row(leader_xt,leader_vt,leader_at))

pos, spd, acc = plot_xva(time, X, V, A)
show(row(pos,spd, acc))


#%%

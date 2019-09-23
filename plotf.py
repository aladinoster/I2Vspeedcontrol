from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.io import output_notebook
from bokeh.palettes import Viridis256

from carfollow import U_I


def map_vc(v):
    return Viridis256[int(min(((U_I - v) / U_I), 1) * 255)]


def plot_trj(time, data_x, data_v):
    p = figure(title="Trajectories")
    for i, data in enumerate(zip(data_x.T, data_v.T)):
        x, v = data
        colors = [map_vc(c) for c in v[:-1]]
        p.scatter(time, x[:-1], color=colors, radius=0.5)
        p.line(time, x[:-1], color="gainsboro")
    return p

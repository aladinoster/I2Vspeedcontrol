from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.io import output_notebook
from bokeh.palettes import Viridis256, Set1
from bokeh.transform import linear_cmap
from bokeh.models import ColumnDataSource, ColorBar
import numpy as np

from carfollow import U_I


def map_vc(v):
    val = max(0, min(((U_I - v) / U_I), 1))  # Clamp values [0, 1]
    return Viridis256[int(val * 255)]


def plot_single_trajectory(p, x, y, c, mapper):

    source = ColumnDataSource(dict(x=x, y=y, color=c))
    p.circle(x="x", y="y", line_color=mapper, color=mapper, fill_alpha=1, size=1, source=source)
    p.line(x, y, color="gainsboro")
    return p


def plot_trj(data_x, data_y, data_color, title="Curve vs time"):

    p = figure(title=title, plot_height=500, plot_width=500)

    color_min, color_max = np.min(data_color), np.max(data_color)

    revViridis256 = list(reversed(Viridis256))
    mapper = linear_cmap(field_name="color", palette=revViridis256, low=color_min, high=color_max)

    for i, data in enumerate(zip(data_y.T, data_color.T)):
        y, c = data
        p = plot_single_trajectory(p, data_x, y[:-1], c[:-1], mapper)

    color_bar = ColorBar(color_mapper=mapper["transform"], width=8, location=(0, 0))
    p.add_layout(color_bar, "right")
    p.xaxis.axis_label = "Time [secs]"
    return p


def plot_leader_acc(time, lead_acc):
    """ Plots leaders acceleration """
    leader = figure(title="Leader's acceleration", plot_height=500, plot_width=500)
    leader.line(time, lead_acc)
    leader.xaxis.axis_label = "Time [secs]"
    leader.yaxis.axis_label = "Acceleration [m/s²]"
    return leader

from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.io import output_notebook
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap
from bokeh.models import ColumnDataSource, ColorBar
import numpy as np

from carfollow import U_I


def plot_single_trajectory(p, x, y, c, mapper):
    """ Daraws a single trajectory"""
    source = ColumnDataSource(dict(x=x, y=y, color=c))
    p.circle(x="x", y="y", line_color=mapper, color=mapper, fill_alpha=1, size=2, source=source)
    p.line(x, y, color="gainsboro")
    return p


def get_mapper(data_mapper):
    """ Color mapper"""
    color_min, color_max = np.min(data_mapper), np.max(data_mapper)

    revViridis256 = list(reversed(Viridis256))
    mapper = linear_cmap(field_name="color", palette=revViridis256, low=color_min, high=color_max)
    return mapper


def post_decoration(p, mapper, xlabel, ylabel):
    """ add colorbar + labels """
    color_bar = ColorBar(color_mapper=mapper["transform"], width=8, location=(0, 0))
    p.add_layout(color_bar, "right")
    p.xaxis.axis_label = xlabel
    p.yaxis.axis_label = ylabel
    return p


def plot_multiple_trajectories(data_x, data_y, data_color, title=None, xlabel=None, ylabel=None):
    """ Draw multiple trajectories"""
    p = figure(title=title, plot_height=500, plot_width=500)

    mapper = get_mapper(data_color)

    for i, data in enumerate(zip(data_y.T, data_color.T)):
        y, c = data
        p = plot_single_trajectory(p, data_x, y[:-1], c[:-1], mapper)

    p = post_decoration(p, mapper, xlabel, ylabel)
    return p


def plot_single_trace(data_x, data_y, title=None, xlabel=None, ylabel=None):
    """ Plots a single trace """

    p = figure(title=title, plot_height=500, plot_width=500)

    mapper = get_mapper(data_y)

    p = plot_single_trajectory(p, data_x, data_y, data_y, mapper)

    p = post_decoration(p, mapper, xlabel, ylabel)
    return p


def plot_xva(time, x, v, a):
    """ Plots all trajectories pos, speed acceleration"""
    pos = plot_multiple_trajectories(time, x, v, "Position", "Time [secs]", "Position [m]")
    spd = plot_multiple_trajectories(time, v, v, "Speed", "Time [secs]", "Speed [m/s]")
    acc = plot_multiple_trajectories(
        time, a, a, "Acceleration", "Time [secs]", "Acceleration [m/s²]"
    )

    return (pos, spd, acc)

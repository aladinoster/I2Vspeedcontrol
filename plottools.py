from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.io import output_notebook
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap
from bokeh.models import ColumnDataSource, ColorBar, Span
import numpy as np

from carfollow import U_I


def plot_single_trajectory(p, x, y, c, mapper,size=2):
    """ Daraws a single trajectory"""
    source = ColumnDataSource(dict(x=x, y=y, color=c))
    p.circle(x="x", y="y", line_color=mapper, color=mapper, fill_alpha=1, size=size, source=source)
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


def plot_multiple_trajectories(
    data_x,
    data_y,
    data_color,
    title=None,
    xlabel=None,
    ylabel=None,
    x_range=(0, 800),
    y_range=(0, 20000),
):
    """ Draw multiple trajectories"""
    p = figure(
        title=title, tools=[], plot_height=500, plot_width=500, x_range=x_range, y_range=y_range
    )

    mapper = get_mapper(data_color)
    p.toolbar.logo = None
    p.toolbar_location = None

    for i, data in enumerate(zip(data_y.T, data_color.T)):
        y, c = data
        p = plot_single_trajectory(p, data_x, y, c, mapper)

    p = post_decoration(p, mapper, xlabel, ylabel)
    return p


def plot_single_trace(data_x, data_y, title=None, xlabel=None, ylabel=None, p_height=500, p_width=500):
    """ Plots a single trace """

    p = figure(title=title, plot_height=p_height, plot_width=p_width)
    p.yaxis.axis_label_text_font_size='14pt'
    p.yaxis.major_label_text_font_size='14pt'
    p.xaxis.axis_label_text_font_size='14pt'
    p.xaxis.major_label_text_font_size='14pt'    
    
    mapper = get_mapper(data_y)

    p = plot_single_trajectory(p, data_x, data_y, data_y, mapper, 4)

    p = post_decoration(p, mapper, xlabel, ylabel)
    return p


def plot_xva(time, x, v, a, y_range, titles):
    """ Plots all trajectories pos, speed acceleration"""
    pos_zoom, spd_zoom, acc_zoom = y_range
    pos_tit, spd_tit, acc_tit = titles
    pos = plot_multiple_trajectories(
        time, x, v, pos_tit, "Time [secs]", "Position [m]", y_range=pos_zoom
    )
    spd = plot_multiple_trajectories(
        time, v, v, spd_tit, "Time [secs]", "Speed [m/s]", y_range=spd_zoom
    )
    acc = plot_multiple_trajectories(
        time, a, a, acc_tit, "Time [secs]", "Acceleration [m/s²]", y_range=acc_zoom
    )

    return (pos, spd, acc)


def plot_histogram(data_x, var_name=None):
    """ Plots histogram of data"""

    hist, edges = np.histogram(data_x, density=True)
    p = figure(title="Histogram", plot_height=500, plot_width=500, background_fill_color="#fafafa")
    p.quad(
        top=hist,
        bottom=0,
        left=edges[:-1],
        right=edges[1:],
        fill_color="navy",
        line_color="white",
        alpha=0.5,
    )
    p.yaxis.axis_label_text_font_size='13pt'
    p.yaxis.major_label_text_font_size='13pt'
    p.xaxis.axis_label_text_font_size='13pt'
    p.xaxis.major_label_text_font_size='13pt'        
    mean = Span(location=np.mean(data_x), dimension="height", line_color="red", line_width=1)
    p.add_layout(mean)
    p.xaxis.axis_label = var_name
    p.yaxis.axis_label = "Density"
    p.grid.grid_line_color = "white"
    return p


def plot_stairs(data_x, data_y, title=None, xlabel=None, ylabel=None):
    """ Plot stairs plot"""
    p = figure(title=title, plot_height=500, plot_width=500)
    p.step(data_x, data_y, line_width=2, mode="before")
    p.xaxis.axis_label = xlabel
    p.yaxis.axis_label = ylabel
    return p

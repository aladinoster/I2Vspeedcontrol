from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.io import output_notebook
from bokeh.palettes import Viridis256, Set1
from bokeh.models import ColorBar, LinearColorMapper

from carfollow import U_I


def map_vc(v):
    val = max(0, min(((U_I - v) / U_I), 1))  # Clamp values [0, 1]
    return Viridis256[int(val * 255)]


def plot_trj(time, data_x, data_v, title="Curve vs time"):
    p = figure(title=title, plot_height=500, plot_width=500)
    v = range(0, 25)
    # color_mapper = LinearColorMapper(
    #     palette="Viridis256", high_color=Viridis256[255], low_color=Viridis256[255]
    # )
    # color_bar = ColorBar(color_mapper=color_mapper, border_line_color=None, location=(0, 0))
    for i, data in enumerate(zip(data_x.T, data_v.T)):
        x, v = data
        colors = [map_vc(c) for c in v[:-1]]
        p.scatter(time, x[:-1], color=colors, radius=0.3)
        # p.line(time, x[:-1], color=Set1[9][i])
        p.line(time, x[:-1], color="gainsboro")
    # p.add_layout(color_bar, "right")
    return p

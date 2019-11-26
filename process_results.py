""" 
    Process results 

    This script process results for the final report of SCOOP

"""

# ==============================================================================
# Imports
# ==============================================================================

import pandas as pd
from matplotlib import pyplot as plt

from matplotlib import rc

rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=True)

from glob import glob
import re

# ==============================================================================
# Constants
# ==============================================================================

ddir_lst = ["data/eu4dpfmix_mpr0.csv", "data/eu4dpfmix.csv"]

# ==============================================================================
# Functions
# ==============================================================================


def column_generator(data_frame):
    """ 
        Create supplementary columns 
    """

    str_splt = data_frame["Cycle"].split("-")
    veh_id = int(str_splt[0])
    mpr = float(str_splt[2].split("_")[0])
    flow = float(str_splt[3].split("_")[0])
    distance = int(str_splt[4].split(".dri")[0])
    return pd.Series([veh_id, mpr, flow, distance])


def create_columns(data_frame, function):
    """
        Apply function to dataframe 
    """
    fields = ["veh_id", "mpr", "flow", "distance"]
    data_frame[fields] = data_frame.apply(function, axis=1)
    return data_frame


def refer_to_mpr(data_frame, field, new_field):
    """
        Refer to MPR 0 %
    """
    # Create reference data_frame

    reference = data_frame[data_frame["mpr"].eq(0)]
    reference = pd.concat([reference] * 5).reset_index()
    reference = reference.drop("index", axis=1)

    # Compute difference
    diff_df = reference[field] - data_frame[field]
    # diff_df = diff_df.reset_index()
    data_frame[new_field] = (diff_df.divide(reference[field])) * 100

    # Round for results
    data_frame = data_frame.round(3)

    return data_frame


def plot_var(
    data_frame,
    x_var="flow",
    y_var="CO_TP",
    label_var="mpr",
    pivot="distance",
    x_label="Flow [veh/m]",
    y_label="CO2 %",
    t_label="Distance [m]: ",
    legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
    fnt_size={"fontsize": 16},
    x_size=5,
    y_size=7.5,
    transpose=False,
):
    """
        Plot variables
    """

    pivoter = data_frame[pivot].unique()
    N = len(pivoter)
    if transpose:
        n, m = 1, N
    else:
        m, n = 1, N

    fig, axes = plt.subplots(m, n, figsize=(x_size * N, y_size), sharey=True)

    for pvt, ax in zip(pivoter, axes):
        flt = data_frame[pivot].eq(pvt)
        df = data_frame[flt]
        df.pivot_table(
            index=x_var, columns=label_var, values=y_var, aggfunc="mean"
        ).plot(kind="bar", ax=ax, grid=True)
        ax.set_xlabel(x_label, fontdict=fnt_size)
        ax.set_ylabel(y_label, fontdict=fnt_size)
        ax.set_title(t_label + str(pvt), fontdict=fnt_size)
        ax.legend(legends)

    return fig, axes


def plot_co2perc(data_frame):
    """
        Create Dataframe CO2 % Data vs flow
    """
    figco2, axco2 = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="CO2 %",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label=r"Change in CO$_2$ [\%]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )

    return figco2, axco2


def plot_co2(data_frame):
    """
        Create Dataframe CO2 consumption vs flow
    """
    figco2, axco2 = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="CO2_TP",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label="CO$_2$ [g/km]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )

    for ax in axco2:
        ax.set(ylim=(120, 160))

    return figco2, axco2


def plot_ttt(data_frame):
    """ 
        Plot absolute Total Travel Time vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="totalTT",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label="Total Travel Time [s]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_tttprc(data_frame):
    """ 
        Plot Change Total Travel Time % vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="totTT %",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label=r"Change in Total TT [\%]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_tttd(data_frame):
    """ 
        Plot Absolute Total Travel Time vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="totalTT",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label="Total Travel Time [s]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_tttdprc(data_frame):
    """ 
        Plot Change Total Travel Time % vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="totTT %",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label=r"Change in Total TT [\%]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_mtt(data_frame):
    """ 
        Plot absolute Avg Travel Time vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="meanTT",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label="Avg. Travel Time [s]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_mttperc(data_frame):
    """ 
        Plot Change Avg Travel Time % vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="avgTT %",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label=r"Change in Avg. TT [\%]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_mttd(data_frame):
    """ 
        Plot Absolute Total Travel Time vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="meanTT",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label="Average Travel Time [s]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_mttdprc(data_frame):
    """ 
        Plot Change Total Travel Time % vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="avgTT %",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label=r"Change in Avg. TT [\%]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_ttc(data_frame):
    """ 
        Plot time to Colission vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="timetC",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label="Time To Collision [s]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_ttcprc(data_frame):
    """ 
        Plot Change Total Travel Time % vs flow
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="flow",
        y_var="timeTC %",
        label_var="mpr",
        pivot="distance",
        x_label="Flow [veh/m]",
        y_label=r"Change in Time to Collision [\%]",
        t_label="Distance [m]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_ttcd(data_frame):
    """ 
        Plot Absolute Total Travel Time vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="timetC",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label="Time To Collision [s]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_ttcdprc(data_frame):
    """ 
        Plot Change Total Travel Time % vs distance
    """
    figtt, axtt = plot_var(
        data_frame=data_frame,
        x_var="distance",
        y_var="timeTC %",
        label_var="mpr",
        pivot="flow",
        x_label="Distance [m]",
        y_label=r"Change in Time to Collision [\%]",
        t_label="Flow [veh/h]: ",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
    )
    return figtt, axtt


def plot_hwy(data_frame):
    """ 
        Plot spacing vs time 
    """
    fighwy, axhwy = plot_var(
        data_frame=data_frame,
        x_var="time",
        y_var="hwy",
        label_var="mpr",
        pivot="flow",
        x_label=" Time [hh:mm]",
        y_label="Headway space [m]",
        t_label="Flow [veh/h]",
        legends=[r"0 \%", r"10 \%", r"20 \%", r"30 \%", r"40 \%"],
        fnt_size={"fontsize": 16},
        x_size=7.5,
        transpose=True,
    )
    return fighwy, axhwy


# ==============================================================================
# Processing
# ==============================================================================

# CO2
# ==============================================================================

# Import csv files
dflst = [pd.read_csv(file) for file in ddir_lst]
fltstr = "PC_EU4_D_DPFMix_HBEFA41.gen"
dflst = [df[df["Input File"].eq(fltstr)] for df in dflst]

# Combine data + column selection
sel_cols = ["Input File", "Cycle", "CO2_TP"]
co2_df = pd.concat([x.filter(items=sel_cols) for x in dflst])
co2_df = co2_df.reset_index()

# Create supplementary columns
co2_df = create_columns(co2_df, column_generator)
co2_df = co2_df.filter(items=["CO2_TP", "veh_id", "mpr", "flow", "distance"])

# Replace values
co2_df["mpr"] = co2_df["mpr"] * 100  # Flow
co2_df["flow"] = co2_df["flow"] * 2880

# Refer data to MPR 0%
co2prc_df = refer_to_mpr(co2_df, "CO2_TP", "CO2 %")

# Plot CO 2 % vs Flow
figco2, axco2 = plot_co2(co2prc_df)
plt.savefig("data/img/summary/CO2vsFlow.png")

figco2prc, axco2prc = plot_co2perc(co2prc_df)
plt.savefig("data/img/summary/CO2%vsFlow.png")
# plt.show()

# Travel Time
# ==============================================================================

# Import csv files
tt_df = pd.read_csv(
    "data/Indicators.csv",
    names=["mpr", "flow", "distance", "meanTT", "stdTT", "totalTT", "timetC"],
)

# Replace values
tt_df = tt_df.drop_duplicates()
tt_df["flow"] = tt_df["flow"] * 3600

# Refer to data MPR 0%
avgtt_df = refer_to_mpr(tt_df, "meanTT", "avgTT %")
tottt_df = refer_to_mpr(tt_df, "totalTT", "totTT %")
timtc_df = refer_to_mpr(tt_df, "timetC", "timeTC %")

# Average Travel Time
# ==============================================================================

# Plot Avg TT vs Flow
figmtt, axmtt = plot_mtt(avgtt_df)
plt.savefig("data/img/summary/avgTTvsFlow.png")

# Plot Avg TT % Change vs Flow
figmttprc, axmttprc = plot_mttperc(avgtt_df)
plt.savefig("data/img/summary/avgTT%vsFlow.png")

# Plot Avg TT vs distance
figmttd, axmttd = plot_mttd(avgtt_df)
plt.savefig("data/img/summary/avgTTvsDistance.png")

# Plot Avg TT % Change vs distance
figmttdprc, axmttdprc = plot_mttdprc(avgtt_df)
plt.savefig("data/img/summary/avgTT%vsDistance.png")

# Total Travel Time
# ==============================================================================

# Plot total TT vs Flow
figttt, axttt = plot_ttt(tottt_df)
plt.savefig("data/img/summary/totalTTvsFlow.png")

# Plot total TT % Change vs Flow
figtttprc, axtttprc = plot_tttprc(tottt_df)
plt.savefig("data/img/summary/totalTT%vsFlow.png")

# Plot total TT vs distance
figtttd, axtttd = plot_tttd(tottt_df)
plt.savefig("data/img/summary/totalTTvsDistance.png")

# Plot total TT % Change vs distance
figtttdprc, axtttdprc = plot_tttdprc(tottt_df)
plt.savefig("data/img/summary/totalTT%vsDistance.png")

# Time to Collision
# ==============================================================================

# Plot total TT vs Flow
figttc, axttc = plot_ttc(timtc_df)
plt.savefig("data/img/summary/timeTCvsFlow.png")

# Plot total TT % Change vs Flow
figttcprc, axttcprc = plot_ttcprc(timtc_df)
plt.savefig("data/img/summary/timeTC%vsFlow.png")

# Plot total TT vs distance
figttcd, axttcd = plot_ttcd(timtc_df)
plt.savefig("data/img/summary/timeTCvsDistance.png")

# Plot total TT % Change vs distance
figttcdprc, axttcdprc = plot_ttcdprc(timtc_df)
plt.savefig("data/img/summary/timeTC%vsDistance.png")

# Headway space
# ==============================================================================

files = glob("data/csv/spacing_*.csv")
df_list = []

# Pattern to recover x-0.1
pattern = re.compile(r"[a-z]*-\d*[.]?\d*")

for file in files:
    tmp = pd.read_csv(file, names=["time", "hwy"])
    lst_raw = pattern.findall(file.split(".csv")[0])
    dct_prop = {
        prop.split("-")[0]: float(prop.split("-")[1]) for prop in lst_raw
    }

    tmp["mpr"] = dct_prop["mpr"]
    tmp["flow"] = dct_prop["q"]
    tmp["distance"] = dct_prop["d"]

    df_list.append(tmp)

# Combine everything
df_hwy = pd.concat(df_list)

df_hwy_d = []
plt_hwyd = []

# Plot and save for each distance
# Headway vs
for dst in df_hwy.distance.unique():
    df2plot = df_hwy[df_hwy.distance.eq(dst) & df_hwy.flow.eq(1)]
    df_hwy_d.append(df2plot)

# Manual Pivoting for easyness
# Case 1
case_a = df_hwy_d[0]
df_a = case_a.pivot_table(index="time",columns="mpr",values="hwy",aggfunc="mean").reset_index()

fig, ax = plt.subplots(figsize = (10,7.5))
df_a.plot(ax=ax, grid = True)
ax.set_xlabel("Time [s]",fontdict={"fontsize": 16})
ax.set_ylabel("Avg. Headway Space [m]",fontdict={"fontsize": 16})
ax.set_title("Headway for I2V messages @ 5000 m",fontdict={"fontsize": 16})
plt.savefig("data/img/summary/HwyVsTimeQ1D5000.png")

# Case 2
case_a = df_hwy_d[1]
df_a = case_a.pivot_table(index="time",columns="mpr",values="hwy",aggfunc="mean").reset_index()

fig, ax = plt.subplots(figsize = (10,7.5))
df_a.plot(ax=ax, grid = True)
ax.set_xlabel("Time [s]",fontdict={"fontsize": 16})
ax.set_ylabel("Avg. Headway Space [m]",fontdict={"fontsize": 16})
ax.set_title("Headway for I2V messages @ 10000 m",fontdict={"fontsize": 16})
plt.savefig("data/img/summary/HwyVsTimeQ1D10000.png")

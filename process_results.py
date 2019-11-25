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


def create_columns(data_frame):
    """
        Apply function to dataframe 
    """
    fields = ["veh_id", "mpr", "flow", "distance"]
    data_frame[fields] = data_frame.apply(column_generator, axis=1)
    return data_frame


def refer_to_mpr(data_frame, field):
    """
        Refer to MPR 0 %
    """
    # Create reference data_frame

    reference = data_frame[data_frame["mpr"].eq(0)]
    reference = pd.concat([reference] * 5).reset_index()
    reference = reference.drop("index", axis=1)

    # Compute difference
    diff_df = data_frame[field] - reference[field]
    # diff_df = diff_df.reset_index()
    data_frame["CO2 %"] = (diff_df.divide(reference[field])) * 100

    # Round for results
    data_frame = data_frame.round(3)

    return data_frame


def plot_var(data_frame, variable, x_label, fnt_size={"fontsize": 16}):
    """
        Plot variables
    """
    fig, ax = plt.subplots(1, 2, figsize=(15, 7.5), sharey=True)

    d1 = 5000
    co2prc_df[co2prc_df["distance"].eq(d1)].pivot_table(
        index="flow", columns="mpr", values=variable, aggfunc="mean"
    ).plot(kind="bar", ax=ax[0], grid=True)

    d2 = 10000
    co2prc_df[co2prc_df["distance"].eq(d2)].pivot_table(
        index="flow", columns="mpr", values=variable, aggfunc="mean"
    ).plot(kind="bar", ax=ax[1], grid=True)

    ax[0].set_xlabel("Flow [veh/h]", fontdict=fnt_size)
    ax[0].set_ylabel(x_label, fontdict=fnt_size)
    ax[0].set_title(f"Distance {d1} [m]", fontdict=fnt_size)
    ax[0].legend(["0 \%","10 \%","20 \%","30 \%","40 \%"])

    ax[1].set_xlabel("Flow [veh/h]", fontdict=fnt_size)
    ax[1].set_ylabel(x_label, fontdict=fnt_size)
    ax[1].set_title(f"Distance {d2} [m]", fontdict=fnt_size)
    ax[1].legend(["0 \%","10 \%","20 \%","30 \%","40 \%"])    

    return fig, ax


def plot_co2perc(data_frame):
    """
        Create Dataframe CO2 % Data 
    """
    figco2, axco2 = plot_var(data_frame, "CO2 %", r"Change in CO$_2$ [\%]")

    return figco2, axco2


def plot_co2(data_frame):
    """
        Create Dataframe CO2 consumption
    """
    figco2, axco2 = plot_var(data_frame, "CO2_TP", "CO$_2$ [g/km]")
    axco2[0].set(ylim=(120, 160))
    axco2[1].set(ylim=(120, 160))
    return figco2, axco2


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
co2_df = create_columns(co2_df)
co2_df = co2_df.filter(items=["CO2_TP", "veh_id", "mpr", "flow", "distance"])

# Replace values
co2_df["mpr"] = co2_df["mpr"] * 100  # Flow
co2_df["flow"] = co2_df["flow"] * 2880

# Refer data to MPR 0%
co2prc_df = refer_to_mpr(co2_df, "CO2_TP")

# Plot CO 2 % vs Flow
figco2, axco2 = plot_co2(co2prc_df)
plt.savefig("data/img/summary/CO2vsFlow.png")

figco2, axco2 = plot_co2perc(co2prc_df)
plt.savefig("data/img/summary/CO2%vsFlow.png")
# plt.show()

# Travel Time
# ==============================================================================

# Import csv files
tt_df = pd.read_csv(
    "data/Indicators.csv",
    names=["mpr", "flow", "distance", "meanTT", "stdTT", "totalTT"],
)

# Replace values
tt_df = tt_df.drop_duplicates()
tt_df["flow"] = tt_df["flow"] * 3.6

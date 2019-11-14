
from itertools import product
import pandas as pd
import matplotlib.pyplot as plt

#%%
Q = (0.3, 0.5, 0.75, 1)
MIN_DIST = (5000, 7500, 10000)
MPR = (0, 0.1, 0.2, 0.3, 0.4)

cases = product(MPR, MIN_DIST, Q)
list_cases = list(product(MPR, MIN_DIST, Q))

def df_standard(df):
    """ Standardize cases """
    df["mpr"] = df["mpr"] * 100
    df["flow"] = df["flow"] * 1000
    df = df.round(3)
    return df


df = pd.read_csv(
    "data/Indicators.csv", names=["mpr", "flow", "distance", "meanTT", "stdTT", "totalTT"]
)
df = df_standard(df)
df["flow"] = df["flow"] * 3.6

df = df.drop_duplicates()  # Necessary because the file is appending results

cdf = pd.DataFrame(list_cases, columns=("mpr", "distance", "flow"))
cdf = df_standard(cdf)
cdf["flow"] = cdf["flow"] * 2.88

#%%
def refer_to_mpr(df):
    "Refers to 0"
    reference = df[df["mpr"].eq(0)]
    reference = pd.concat([reference] * 5).reset_index()
    reference = reference.drop("index", axis=1)
    dif1 = reference["totalTT"] - df["totalTT"]
    dif2 = reference["meanTT"] - df["meanTT"]
    df["totalTTperc"] = (dif1.divide(reference["totalTT"])) * 100
    df["meanTTperc"] = (dif2.divide(reference["meanTT"])) * 100
    df = df.round(3)
    return df

df = refer_to_mpr(df)

# Study cases

fig, ax = plt.subplots(1, 2, figsize=(15, 7.5), sharey=True)

# Filter distance @7500 Observe change in Average Travel Time
d1 = 7500
df[df["distance"].eq(d1)].pivot(index="flow", columns="mpr", values="meanTTperc").plot(
    kind="bar", ax=ax[0]
)

# Filter distance @10000 Observe change in Average Travel Time
d2 = 10000
df[df["distance"].eq(d2)].pivot(index="flow", columns="mpr", values="meanTTperc").plot(
    kind="bar", ax=ax[1]
)

ax[0].set_xlabel("Flow [veh/h]", fontdict={"fontsize": 20})
ax[0].set_ylabel("Change Avg Travel Time [%]", fontdict={"fontsize": 20})
ax[0].set_title(f"Distance {d1} [m]", fontdict={"fontsize": 20})
ax[0].grid(True)

ax[1].set_xlabel("Flow [veh/h]", fontdict={"fontsize": 20})
ax[1].set_ylabel("Change Avg Travel Time [%]", fontdict={"fontsize": 20})
ax[1].set_title(f"Distance {d2} [m]", fontdict={"fontsize": 20})
ax[1].grid(True)

plt.savefig("data/percTTvsFlow.png")

fig, ax = plt.subplots(1, 2, figsize=(15, 7.5), sharey=False)

# Filter distance @C/2 Observe change in Average Travel Time vs distance
f1 = 1440
df[df["flow"].eq(f1)].pivot(index="distance", columns="mpr", values="meanTTperc").plot(
    kind="bar", ax=ax[0]
)

# Filter distance @C Observe change in Average Travel Time vs distance
f2 = 2880
df[df["flow"].eq(f2)].pivot(index="distance", columns="mpr", values="meanTTperc").plot(
    kind="bar", ax=ax[1]
)

ax[0].set_xlabel("Distance [m]", fontdict={"fontsize": 20})
ax[0].set_ylabel("Change Avg Travel Time [%]", fontdict={"fontsize": 20})
ax[0].set_title(f"Flow {f1} [veh/h]", fontdict={"fontsize": 20})
ax[0].grid(True)

ax[1].set_xlabel("Distance [m]", fontdict={"fontsize": 20})
ax[1].set_ylabel("Change Avg Travel Time [%]", fontdict={"fontsize": 20})
ax[1].set_title(f"Flow {f2} [veh/h]", fontdict={"fontsize": 20})
ax[1].grid(True)

plt.savefig("data/percTTvsDistance.png")


#%%

dpol = pd.read_csv("data/data_comb.csv")

def generate_cols(df):
    data = df["Cycle"].split("-")
    vid = int(data[0])
    mpr = float(data[2].split("_")[0])
    flow = float(data[3].split("_")[0])
    dist = int(data[4].split(".dri")[0])
    return pd.Series([vid, mpr, flow, dist])


def refer_to_mpr_pol(df):
    "Refers to 0"
    reference = df[df["mpr"].eq(0)]
    reference = pd.concat([reference] * 5).reset_index()
    reference = reference.drop("index", axis=1)
    dif1 = df["CO2_TP"]- reference["CO2_TP"] 
    df["CO2_TPperc"] = (dif1.divide(reference["CO2_TP"])) * 100
    df = df.round(3)
    return df

fields =['vid','mpr','flow','dist']
dpol[fields] = dpol.apply(generate_cols,axis=1)

dpolf=dpol[['CO2_TP','mpr','flow','dist']]
dpolf = dpolf.groupby(['mpr','flow','dist']).sum()
dpolf = dpolf.reset_index()

dpolf['mpr'] = dpolf['mpr'].replace(0.1,0)
dpolf = refer_to_mpr_pol(dpolf)

dpolf['flow'] = dpolf['flow']*2880

fig, ax = plt.subplots(1, 2, figsize=(15, 7.5), sharey=True)

d1 = 5000
dpolf[dpolf["dist"].eq(d1)].pivot(index="flow", columns="mpr", values="CO2_TPperc").plot(
    kind="bar", ax=ax[0]
)

d2 = 10000
dpolf[dpolf["dist"].eq(d2)].pivot(index="flow", columns="mpr", values="CO2_TPperc").plot(
    kind="bar", ax=ax[1]
)

ax[0].set_xlabel("Flow [veh/h]", fontdict={"fontsize": 20})
ax[0].set_ylabel("Change in CO$_2$ [%]", fontdict={"fontsize": 20})
ax[0].set_title(f"Distance {d1} [m]", fontdict={"fontsize": 20})
ax[0].grid(True)

ax[1].set_xlabel("Flow [veh/h]", fontdict={"fontsize": 20})
ax[1].set_ylabel("Change in CO$_2$ [%]", fontdict={"fontsize": 20})
ax[1].set_title(f"Distance {d2} [m]", fontdict={"fontsize": 20})
ax[1].grid(True)

plt.savefig("data/CO2vsFlow.png")
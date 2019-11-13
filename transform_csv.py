"""
    This script is created to transform files in the data/csv folder into 
    dri files for Phem. 
"""

import os
import pandas as pd
import numpy as np

datadir = "data/csv/"
destdir = "data/dri/"
filenames = os.listdir(datadir)

for case, filename in enumerate(filenames):
    basename = filename.split(".csv")[0]
    newfiledir = destdir + str(case) + '/' 
    if not os.path.exists(newfiledir):
        os.makedirs(newfiledir)
    df = pd.read_csv(datadir + filename)
    for idx in df["vehicle number"].unique():
        wfname = newfiledir + str(idx) + "-" + basename +".dri"
        wfileobj = open(wfname, "w")
        wfileobj.write("v2\n")
        wfileobj.write("<t>,<v>,<grad>\n")
        wfileobj.write("[s],[km/h],[%]\n")
        data = df[df["vehicle number"].eq(idx)][["time","speed","road inclination"]].to_numpy()
        np.savetxt(wfileobj,data,delimiter=",",fmt="%.3f")
        wfileobj.close()

import pandas as pd
import numpy as np

def pandas_process(sweep):
    # This first segment is attempting to compress all of the objects into categorical variables
    date = str(sweep['Date'][0]).strip()
    time = str(sweep['Time'][0]).strip()
    bins = str(sweep['hz_bin'][0])
    samples = str(sweep['n_samples'][0])
    sweep = sweep.drop(["Date","Time","n_samples","hz_bin"], axis=1)
    temp = pd.DataFrame(columns=['hz','db'])

    for i, row in sweep.iterrows():
        high = row['hz_high']; low = row['hz_low'];
        r = np.arange(low, high, (high-low)/5) # Five is from the sweep software we're provided
        for c,i in enumerate(r):
            vals = row.iloc[c].drop(labels=["hz_low", "hz_high"])
            temp = temp.append({"hz":i, "db":vals}, ignore_index=True)

    return {
        "date":date,
        "time":time,
        "bins":bins,
        "samples":samples,
        "data":temp.to_json(orient="records")
    }
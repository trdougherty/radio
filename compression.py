from builtins import str
import pandas as pd
import numpy as np

def convert_json(sweep):
    # This first segment is attempting to compress all of the objects into categorical variables
    date = str(sweep['Date'][0]).strip()
    time = str(sweep['Time'][0]).strip()
    bins = str(sweep['hz_bin'][0])
    samples = str(sweep['n_samples'][0])
    sweep = sweep.drop(["Date","Time","n_samples","hz_bin"], axis=1)
    temp = pd.DataFrame(columns=['hz','db'])

    for i, row in sweep.iterrows():
        high = row['hz_high']; low = row['hz_low'];
        r = np.arange(low, high, (high-low) // 5) # Five is from the sweep software we're provided
        for c,i in enumerate(r):
            temp = temp.append({"hz":i, "db":row.iloc[2+c]}, ignore_index=True)

    return {
        "date":date,
        "time":time,
        "bins":bins,
        "samples":samples,
        "data":temp.to_json(orient="records")
    }
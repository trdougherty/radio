import sys
import os
import pandas as pd

from compression import compress

saving = "data"

filename = sys.argv[1] #If this fails it means that the process was involved improperly
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])
scan = compress(scan)

save_name = os.path.splitext(filename)[0] + ".pkl"

if not os.path.exists(saving):
    os.makedirs(saving)

scan.to_pickle(saving+"/"+save_name)
os.remove(filename)

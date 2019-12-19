import sys
import os
import pandas as pd
import json
import compress_json

from compression import convert_json

saving = "data"

filename = sys.argv[1] #If this fails it means that the process was involved improperly
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

# This gets the base name for the file
file_base = os.path.splitext(filename)[0]

# Meat and bones of the processing
json_scan = convert_json(scan)

if not os.path.exists(saving):
    os.makedirs(saving)

compress_json.dump(json_scan, saving+"/"+file_base+".json.gz")
os.remove(filename)

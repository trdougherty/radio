import sys
import os
import json
import pandas as pd
import compress_json

from gps_scan import gps_scan
from compression import convert_json

saving = "data"

filename = sys.argv[1] #If this fails it means that the process was involved improperly
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

# This gets the base name for the file
file_base = os.path.splitext(filename)[0]

# Meat and bones of the processing
json_scan = convert_json(scan)

# GPS data if possible
gps_scan = gps_scan()
if gps_scan:
    json_scan.update(gps_scan)

# Makes the directory if it doesn't already exist
if not os.path.exists(saving):
    os.makedirs(saving)

# Compresses the files so we can save them and removes the uncompressed originals
compress_json.dump(json_scan, saving+"/"+file_base+".json.gz")
os.remove(filename)

import sys
import os
import json
import pandas as pd
import gzip

from gps_scan import gps_scan
from compression import convert_json
from strip_prefix import strip_prefix

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

saving = os.environ.get("SAVE_DIR")
temp = os.environ.get("TEMP_DIR")

filename = sys.argv[1] #If this fails it means that the process was involved improperly
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

# This gets the base name for the file
file_base = os.path.splitext(filename)[0]

# Meat and bones of the processing
json_scan = convert_json(scan)

# GPS data if possible
gps_info = gps_scan()
if gps_info:
    json_scan.update(gps_info)

# Makes the directory if it doesn't already exist
print(saving)
if not os.path.exists(saving):
    os.makedirs(saving)

# Compresses the files so we can save them and removes the uncompressed originals
with gzip.open(saving+"/"+strip_prefix(file_base, temp +"/")+".json.gz", 'wt') as zipfile:
    json.dump(json_scan, zipfile)

os.remove(filename)

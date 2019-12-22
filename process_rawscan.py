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

# This will terminate the program if there is no name. Don't be mean. Give your child a name.
name = os.getenv("NAME")
saving = os.getenv("SAVE_DIR", "data")
temp = os.getenv("TEMP_DIR", "temp")
edge = os.getenv("EDGE", "0")
antenna = os.getenv("ANTENNA", "0")
samples = os.getenv("SAMPLES", "20")
scientist = os.getenv("SCIENTIST")
low = os.getenv("LOW", "0")
high = os.getenv("HIGH", "6000000000")

filename = sys.argv[1] #If this fails it means that the process was involved improperly
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

# This gets the base name for the file
file_base = os.path.splitext(filename)[0]

# GPS data if possible
gps_info = gps_scan()

# Meat and bones of the processing
if bool(int(edge)):
    json_scan = convert_json(scan)
else:
    # This will divy out the processing if it wasn't enabled on the edge computer
    json_scan = scan
    
full_data = {
    "metadata": {
        "name": name,
        "scientist": scientist,
        "antenna": antenna,
        "samples": samples,
        "edge": edge,
        "gps": gps_info
    },
    "data": json_scan
}

# Makes the directory if it doesn't already exist
print(saving)
if not os.path.exists(saving):
    os.makedirs(saving)

# Compresses the files so we can save them and removes the uncompressed originals
js_dumps = json.dumps(full_data)
with gzip.open(saving+"/"+strip_prefix(file_base, temp +"/")+".json.gz","w") as f:
    f.write(js_dumps)

os.remove(filename)
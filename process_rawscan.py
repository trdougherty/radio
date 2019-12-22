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
from json_zip import json_zip

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# This will terminate the program if there is no name. Don't be mean. Give your child a name.
name = os.getenv("NAME")
temp = os.getenv("TEMP_DIR", "temp")
edge = os.getenv("EDGE", "0")
antenna = os.getenv("ANTENNA", "0")
samples = os.getenv("SAMPLES", "20")
scientist = os.getenv("SCIENTIST")
low = os.getenv("LOW", "0")
high = os.getenv("HIGH", "6000000000")

print "Arguments: ", sys.argv

filename = sys.argv[1] #If this fails it means that the process was involved improperly
print "Extracting file from: ", filename
file_base = os.path.splitext(filename)[0] # Base name of the file

saving = sys.argv[2] #The storage directory
print "Target save folder: ", storage

# Extracts the scan from temp storage
scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

# GPS data if possible
gps_info = gps_scan()

# Meat and bones of the processing
if bool(int(edge)):
    # This should work..? Haven't really tested it
    json_scan = convert_json(scan) # -> this will return a dictionary
else:
    # This will divy out the processing if it wasn't enabled on the edge computer
    json_scan = scan.to_json(orient='records') # -> this returns a pretty big string
    
full_data = {
    "metadata": {
        "name": name,
        "scientist": scientist,
        "antenna": antenna,
        "samples": samples,
        "edge": edge,
        "gps": gps_info
    },
    "data": json_zip(json_scan)
}

# Makes the directory if it doesn't already exist
if not os.path.exists(saving):
    os.makedirs(saving)

# Yeah going to just leave this for now because it works and 
with open(saving+"/"+strip_prefix(file_base, temp +"/")+".json",'w') as f:
    json.dump(full_data, f)

os.remove(filename)

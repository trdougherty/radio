from __future__ import print_function
import sys
import os
import json
import pandas as pd
import gzip
import time

from gps_scan import gps_scan
from compression import convert_json
from strip_prefix import strip_prefix
from gpiozero import LED
from pandas_process import pandas_process

from os.path import join, dirname, realpath, splitext
from dotenv import load_dotenv
from json_zip import json_zip

dotenv_path = join(dirname(realpath(__file__)), '.env')
gpio_info = join(dirname(realpath(__file__)), '.gpio_env')
load_dotenv(dotenv_path)
load_dotenv(gpio_info)

gpio_bool = os.getenv("GPIO")

if gpio_bool:
    red = os.getenv("RED")
    error_led = LED(red)

# This will terminate the program if there is no name. Don't be mean. Give your child a name.
try:
    name = os.getenv("NAME")
    temp = os.getenv("TEMP_DIR", "temp")
    edge = os.getenv("EDGE", "0")
    antenna = os.getenv("ANTENNA", "0")
    samples = os.getenv("SAMPLES", "20")
    scientist = os.getenv("SCIENTIST")
    low = os.getenv("LOW", "0")
    high = os.getenv("HIGH", "6000000000")
    storage = os.getenv("STORAGE", "storage")

    # Current path
    current_path = dirname(realpath(__file__))

    arguments = sys.argv
    print("Arguments: ", arguments)

    filename = arguments[1] #If this fails it means that the process was involved improperly
    print("Extracting file from: ", filename)

    file_base = splitext(filename)[0] # Base name of the file

    saving = join(current_path, storage) #The storage directory
    print("Target save folder: ", saving)

    # Extracts the scan from temp storage
    scan = pd.read_csv(filename, delimiter=",", names=["Date","Time","hz_low","hz_high","hz_bin","n_samples","db1","db2","db3","db4","db5"])

    # GPS data if possible
    gps_info = gps_scan()
    
    if bool(int(edge)):
        scan = pandas_process(scan) # -> this will return a dictionary
        
    # Meat and bones of the processing
    json_scan = scan.to_json(orient='records')
        
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

    with open(saving+"/"+strip_prefix(file_base, temp +"/")+".json",'w') as f:
        json.dump(full_data, f)

    os.remove(filename)

except:
    if gpio_bool: 
        error_led.on()
        time.sleep(5)
        error_led.off()
    sys.exit(1)
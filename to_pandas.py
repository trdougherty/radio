import os
import sys
import dotenv
import pandas as pd
import json

from os.path import join, abspath, realpath, dirname

from json_unzip import json_unzip
from compression import convert_json

def decompress(incoming):
    with open(incoming, 'r') as f:
        payload = json.load(f)
    
    compressed_data = payload['data']
    data = json_unzip(compressed_data)
    pandas_df = pd.read_json(data, orient='records')
    
    compressed = convert_json(pandas_df)
    return compressed



if __name__ == "__main__":
    filename = join(dirname(__file__), "data/storage/2019-12-23T03:04:53Z.json")
    d = decompress(filename);
    print d['data']
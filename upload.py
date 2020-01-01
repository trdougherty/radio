import os, sys
import json
import requests
import time

import dotenv
dotenv.load_dotenv(verbose=True)

# Local terms
from encoder import encoder, string_normalization

remote = os.getenv('REMOTE')
public_keyname = os.getenv('PUBLIC_KEY')
error_dir = os.getenv('ERROR_FILES')

def strip_right(text, suffix):
    text = text.rsplit('/', 1)[-1] # removes the directories from the filename
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]

def upload(directory, filename):
    filename_full = os.path.abspath(os.path.join(directory, filename))
    error_fullpath = os.path.abspath(os.path.join(os.path.dirname(__file__),error_dir))
    try:
        with open(filename_full, 'r') as f:
            d = json.load(f)
        
        assert d # This validates that we have something here
        assert isinstance(d, dict) # Validates that we have a dictionary
        
        name_kernel = strip_right(filename, '.json')
        
        d.update({ 'name': name_kernel })
        d_string = json.dumps(d)
        encoded = encoder(d_string, public_keyname)
        req = requests.post(remote, json=encoded)
        print req.status_code
        if (req.status_code == 200): #aka data was successfully recieved and interpreted without a problem
            os.remove(filename_full)
            return
        # We got rate limited - need to wait for next upload
        elif (req.status_code == 429):
            time.sleep(10)
            return
        else:
            print "Failed to upload - need to make new folder."
            if not os.path.isdir(error_fullpath): os.makedirs(error_fullpath)
            os.rename(filename_full, os.path.join(error_fullpath, filename))
            return
    except requests.exceptions.RequestException as e:
        print "Reuqest exception! Failed with error: ",e
    except AssertionError as e:
        print "JSON term is null - could not be loaded from data. Failed with error: ", e
    except IOError as e:
        print "Could not open file. Failed with error: ", e
    except ValueError as e:
        print "Error with JSON interpretation. Failed with error: ", e
    except Exception as e:
        print "EXCEPTION: ",e.message, e.args
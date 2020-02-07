from __future__ import print_function
import os, sys
from os.path import join, dirname, realpath, splitext
from dotenv import load_dotenv

import json
import requests
import time
from gpiozero import LED

# Local terms
from encoder import encoder, string_normalization

dotenv_path = join(dirname(realpath(__file__)), '.env')
gpio_info = join(dirname(realpath(__file__)), '.gpio_env')
load_dotenv(dotenv_path)
load_dotenv(gpio_info)

remote = os.getenv('REMOTE')
public_keyname = os.getenv('PUBLIC_KEY')
error_dir = os.getenv('ERROR_FILES')
gpio_bool = os.getenv("GPIO")

if bool(gpio_bool):
    white = os.getenv("WHITE")
    red = os.getenv("RED")
    error_led = LED(red)
    upload_led = LED(white)

def strip_right(text, suffix):
    text = text.rsplit('/', 1)[-1] # removes the directories from the filename
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]

def upload(directory, filename):
    filename_full = os.path.abspath(os.path.join(directory, filename))
    error_fullpath = os.path.abspath(os.path.join(os.path.dirname(__file__),error_dir))
    # This is where we gather the upload data
    with open(filename_full, 'r') as f:
        d = json.load(f)
    
    assert d # This validates that we have something here
    assert isinstance(d, dict) # Validates that we have a dictionary
    
    name_kernel = strip_right(filename, '.json')
    
    d.update({ 'name': name_kernel })
    d_string = json.dumps(d)
    print(type(d_string))
    
    encoded = encoder(d_string, public_keyname)
    for i in encoded.keys():
        current_type = type(encoded[i])
        print(f"{i} type: {current_type}")

    req = requests.post(remote, json=encoded)
    print(req.status_code)
    if (req.status_code == 200): #aka data was successfully recieved and interpreted without a problem
        if gpio_bool:
            upload_led.on()
            time.sleep(1)
            upload_led.off()
        os.remove(filename_full)
        return
    # We got rate limited - need to wait for next upload
    elif (req.status_code == 429):
        if gpio_bool: error_led.on()
        time.sleep(10)
        if gpio_bool: error_led.off()
        return
    else:
        if gpio_bool: error_led.on()
        if not os.path.isdir(error_fullpath): os.makedirs(error_fullpath)
        os.rename(filename_full, os.path.join(error_fullpath, filename))
        time.sleep(3)
        if gpio_bool: error_led.off()
        return
    # except requests.exceptions.RequestException as e:
    #     print("Reuqest exception! Failed with error: ",e)
    # except AssertionError as e:
    #     print("JSON term is null - could not be loaded from data. Failed with error: ", e)
    # except IOError as e:
    #     print("Could not open file. Failed with error: ", e)
    # except ValueError as e:
    #     print("Error with JSON interpretation. Failed with error: ", e)
    # except Exception as e:
    #     print("EXCEPTION: ", e)

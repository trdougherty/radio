#!/usr/bin/python

import os
import time
import dotenv
dotenv.load_dotenv()

# Local functions
from upload import upload
from gpiozero import LED


def files(path):
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            yield filename

if __name__ == "__main__":
    storage = os.getenv('LOCAL_STORAGE', 'storage')
    storage_fullname = os.path.join(os.path.dirname(os.path.abspath(__file__)),storage)
    while True:
        if os.path.isdir(storage_fullname):
            print('Found File Directory: {}'.format(storage_fullname))
            for f in files(storage_fullname):
                print('Current file uploading: {}'.format(f))
                upload(storage_fullname, f)
            time.sleep(2)
        else:
            os.mkdir(storage_fullname)
            # except Exception as e:
            #     print(f"Upload failed with exception: {e}")
            #     break # This cuts on a network loss hopefully


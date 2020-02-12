#!/usr/bin/python

from __future__ import print_function
import serial
import time
import os
import gps

from dotenv import load_dotenv
load_dotenv(verbose=True)

def gps_scan():
	try:
		found = helper()
		if found:
			return {
				"lat": found["lat"],
				"lon": found["lon"],
				"alt": found["alt"]
			}
		return None
	except Exception as e:
		print(e)
		return None

def get_time():
	found = helper()
	if found:
		return found["time"]
	else:
		return None

def helper():
	# Setting initial terms so we can run scans
	try:
		counter = 0
		initial_terms = 0
		returning = {}
		print('Initiating GPS scan...')
		m_gps = gps.GPS()
		while counter < int(os.getenv("GPS_SCANS", 3)):
			print('Waiting for fix...')
			counter += 1
			gps_data = m_gps.gather()
			if gps_data:
				ts = bool(gps_data["time"])
				lat = bool(gps_data["lat"])
				lon = bool(gps_data["lon"])
				alt = bool(gps_data["alt"])
			else:
				ts = lat = lon = alt = False
				time.sleep(1)

			count = ts + lat + lon + alt
			if count > initial_terms:
				returning = gps_data
				initial_terms = count
		
		return returning
	except Exception as e:
		print(e)
		return None

if __name__ == "__main__":
    returning = gps_scan()
    print(returning)

import serial
import pynmea2
import time
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

def gps_scan():
	# All specific to the rapsberrypi's UART communication
	serialStream = serial.Serial(os.getenv("PORT"), os.getenv("BAUD"), timeout=0.5)
	start = end = time.time()
	while end - start < 5:
		end = time.time()
		sentence = serialStream.readline()
		if sentence.find('GGA') > 0:
			try:
				data = pynmea2.parse(sentence)
				if not data.geo_sep:
					data.altitude = None

				return {
					"lat": data.latitude,
					"lon": data.longitude,
					"alt": data.altitude
				}

			except:
				pass

	return None

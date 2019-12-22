import serial
import pynmea2
import time
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

def gps_scan():
	# All specific to the rapsberrypi's UART communication
	serialStream = serial.Serial(os.getenv("PORT", "/dev/ttyAMA0"), os.getenv("BAUD", "9600"), timeout=0.5)
	start = end = time.time()
	while True: #end - start < 5:
		end = time.time()
		sentence = serialStream.readline()
		if sentence.find('GGA') > 0:
			try:
				data = pynmea2.parse(sentence, check=False)
				if not data.geo_sep:
					data.altitude = None
     
				time = data.timestamp
				print time
				gps_data = {
					"lat": data.latitude,
					"lon": data.longitude,
					"alt": data.altitude
				}
				print gps_data
				return gps_data

			except:
				pass

	return None

if __name__ == "__main__":
    gps_scan()
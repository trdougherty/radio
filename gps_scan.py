import serial
import pynmea2
import time

def capture_gps():
    serialStream = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
while True:
    sentence = serialStream.readline()
    if sentence.find('GGA') > 0:
    	try:
            data = pynmea2.parse(sentence)
	    if !data.geo_sep:
	        data.altitude = None

            gps_data = {
		"lat": data.latitude,
	    	"lon": data.longitude,
	    	"alt": data.altitude
	    }
	    return gps_data;
        except:
            print "Failed"
	    return None

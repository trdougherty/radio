source .env

## This section is specific to raspberrypi for debugging and logging
echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction

while true; do
	CON=$(ping -c 1 google.com | wc -l)
	# This line is to indicate the status of the wifi
	echo $CON > /sys/class/gpio/gpio17/value
	if [ $CON -gt 0 ]; then 
		printf "Uploading...\n"
		python upload_manager.py
	else
		sleep 10
	fi
done


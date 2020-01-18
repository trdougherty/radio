source .env

## This section is specific to raspberrypi for debugging and logging
echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction

while true; do
	if [ $CON -gt 0 ]; then 
		printf "Uploading...\n"
		python upload_manager.py
	else
		sleep 10
	fi
done


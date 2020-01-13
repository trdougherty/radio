# Load env variables
source .env

echo "23" > /sys/class/gpio/export  
# Sets pin 18 as an output
echo "out" > /sys/class/gpio/gpio23/direction
echo "0" > /sys/class/gpio/gpio23/value

printf "Scanning Commence.\n"
# Shows the time in universal formatting
D=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
temp_filename=$D".txt"
printf $temp_filename"\n"

# gets the temp directory ready to roll
mkdir -p ${TEMP_DIR:="temp"}
timeout -k 10 5 hackrf_sweep -1 -r $TEMP_DIR/$temp_filename 2> bash_error.txt

if [ -s $TEMP_DIR/$temp_filename ];
then
    printf "Processing scan..."
    head $TEMP_DIR/$temp_filename
    printf "\n"
    python process_rawscan.py $TEMP_DIR/$temp_filename 2> python_error.txt
else	
<<<<<<< HEAD
    echo "Process failed.\n\n"
    echo "1" > /sys/class/gpio/gpio23/value
fi
=======
    printf "Process failed.\n\n"
fi
>>>>>>> 719141ee3ab1a7dfc787f0cfe5aa5e07faf78c90

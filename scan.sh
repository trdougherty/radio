# Load env variables
source .env
source .gpio_env

source ./gpio.sh # gathers all of the functions we want
trap shutdown SIGINT # This will turn all the lights off and shut the program down
setup # sourced from gpio - this gets all of our pins ready

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
    echo "Process failed.\n\n"
    # This flashes a warning sign
    setLightState $RED $ON 1
    setLightState $RED $OFF
fi

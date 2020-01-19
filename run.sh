source .env
source .gpio_env

# Import Three-Finger Claw as TFC
# yell() { echo "$0: $*" >&2; }
# die() { yell "$*"; exit 111; }
# try() { "$@" || die "cannot $*"; }

source ./gpio.sh # gathers all of the functions we want
trap shutdown SIGINT # This will turn all the lights off and shut the program down
setup # sourced from gpio - this gets all of our pins ready

# Sets the gps up
python3 -c "import gps; gps.setup()"

# Check if RTC is up and we've incorporated the correct time into the reading
dt_verify=$(timedatectl | wc -l)
while [ $dt_verify -eq 1 ];
do
    setLightState $RED $ON 1
    setLightState $RED $OFF
    dt_verify=$(timedatectl | wc -l)
    sleep 1
done

while true; do
    {
        HACKRF=$(lsusb | grep HackRF | wc -l)
        if [ $HACKRF -gt 0 ]; then 
            printf "HackRF: %s\n" $HACKRF
            setLightState $BLUE $ON 1
            bash scan.sh
            setLightState $BLUE $OFF
        fi
    } || {
        sleep 10
    }
done

# This needs some work...
# if [ ${MOUNTING:=false} ];then
#     printf "Mounting external drive...\n"
#     STORAGE_DIR=$STORAGE;
#     # try(){ bash mount_storage.sh 2> storage_error.txt };
# else
#     STORAGE_DIR=$LOCAL_STORAGE
# fi
# echo "STORAGE: "$STORAGE_DIR

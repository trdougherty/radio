source .env
source .gpio_env

# Import Three-Finger Claw as TFC
# yell() { echo "$0: $*" >&2; }
# die() { yell "$*"; exit 111; }
# try() { "$@" || die "cannot $*"; }

source ./gpio.sh # gathers all of the functions we want
trap shutdown SIGINT # This will turn all the lights off and shut the program down
setup # sourced from gpio - this gets all of our pins ready

while true; do
    {
        HACKRF=$(lsusb | grep HackRF | wc -l)
        if [ $HACKRF -gt 0 ]; then 
            printf "HackRF: %s\n" $HACKRF
            setLightState $BLUE $ON
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

source .env

# Import Three-Finger Claw as TFC
# yell() { echo "$0: $*" >&2; }
# die() { yell "$*"; exit 111; }
# try() { "$@" || die "cannot $*"; }

## Do something with the RTC
echo "27" > /sys/class/gpio/export  
# Sets pin 18 as an output
echo "out" > /sys/class/gpio/gpio27/direction

while true; do
    # Check if we have internet
    {
        HACKRF=$(lsusb | grep HackRF | wc -l)
        echo $HACKRF > /sys/class/gpio/gpio27/value
        if [ $HACKRF -gt 0 ]; then 
            printf "HackRF: %s\n" $HACKRF
            bash scan.sh
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

source .env

# Import Three-Finger Claw as TFC
# yell() { echo "$0: $*" >&2; }
# die() { yell "$*"; exit 111; }
# try() { "$@" || die "cannot $*"; }

while true; do
    # Check if we have internet
    CON=$(ping -c 1 google.com | wc -l)
    if [ $CON -gt 0 ]; then # For a temporary fix to incorrect time, we're going to only record when we can validate time with the internet
        # Now it checks for the radio - if it exists
        HACKRF=$(lsusb | grep HackRF | wc -l)
        if [ $HACKRF -gt 0 ]; then 
            printf "HackRF: %s\n" $HACKRF
            bash scan.sh
        fi
    else
	sleep 10
        # printf "Capturing time from GPS...\n"
        # RES=$(python -c 'import gps_scan; from gps_scan import get_time; print get_time()')
        # if [ $RES -ne "None" ]; then
        # ## Set time here
        # # sudo date -s $RES
        # CON=1
        # fi
    fi
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

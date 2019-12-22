source .env

# Import Three-Finger Claw as TFC
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# Check if we have internet
CON=$(ping -c 1 google.com | wc -l)
echo "CON: "$CON
if [ $CON -eq 0 ]; then
    printf "Capturing time from GPS...\n"
    RES=$(python -c 'import gps_scan; from gps_scan import get_time; print get_time()')
    if [ $RES -ne "None" ]; then
    ## Set time here
    # sudo date -s $RES
    CON=1
    fi
fi

# Starts mounting process
if [ ${MOUNTING:=false} ];then
    printf "Mounting external drive...\n"
    STORAGE_DIR=$STORAGE;
    # try(){ bash mount_storage.sh 2> storage_error.txt };
else
    STORAGE_DIR=$LOCAL_STORAGE
fi
echo "STORAGE: "$STORAGE_DIR

# Now it checks for the radio - if it exists
if [ !$(lsusb | grep HackRF | wc -l) ]; then 
    printf "Found HackRF. Commencing stage two.\n"
else 
    exit 1
fi

# Scan into oblivion
while true; do
    bash scan.sh $STORAGE_DIR
done

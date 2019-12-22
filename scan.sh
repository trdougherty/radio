# Load env variables
source .env

printf "Scanning Commence.\n"
# Shows the time in universal formatting
D=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
temp_filename=$D".txt"
printf $temp_filename"\n"

# Gets the permanant storage solution which was passed into the system
STORAGE=$1
echo "Input Storage: "$STORAGE

# gets the temp directory ready to roll
mkdir -p ${TEMP_DIR:="temp"}
timeout -k 10 5 hackrf_sweep -1 -r $TEMP_DIR/$temp_filename 2> bash_error.txt

if [ -s $TEMP_DIR/$temp_filename ];
then
    echo "Processing scan..."
    head $TEMP_DIR/$temp_filename
    printf "\n"
    python process_rawscan.py $TEMP_DIR/$temp_filename $STORAGE 2> python_error.txt
else	
    echo "Process failed."
fi

# Load env variables
source .env

# Shows the time in universal formatting
D=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
temp_filename=$D"_sweep.txt"

# gets the temp directory ready to roll
echo $temp_filename
mkdir -p $TEMP_DIR
timeout --signal=SIGQUIT 5 hackrf_sweep -1 -r $TEMP_DIR/$temp_filename 2> bash_error.txt
status=$?
echo $status

if [ ! -s $TEMP_DIR/$temp_filename ];
then
	echo "Processing scan..."
	# Process that text into some kind of meaningful data representation
	python process_rawscan.py $TEMP_DIR/$temp_filename 2> python_error.txt
else	
	echo "Process failed."
	# rm temp/$temp_filename
fi

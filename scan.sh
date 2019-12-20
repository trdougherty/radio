# Shows the time in universal formatting
D=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
temp_filename=$D"_sweep.txt"

# gets the temp directory ready to roll
echo $temp_filename
mkdir -p temp
timeout --signal=SIGQUIT 5 hackrf_sweep -1 -r temp/$temp_filename 2> error.txt
status=$?
echo $status

if [ ! -s temp/$temp_filename ];
then
	echo "Processing scan..."
	# Process that text into some kind of meaningful data representation
	python process_rawscan.py temp/$temp_filename
else	
	echo "Process failed."
	# rm temp/$temp_filename
fi

# Shows the time in universal formatting
D=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
temp_filename=$D"_sweep.txt"

# gets the temp directory ready to roll
mkdir -p temp
hackrf_sweep -1 -r temp/$temp_filename


echo $temp_filename
# Process that text into some kind of meaningful data representation
python process_rawscan.py temp/$temp_filename
source .env

while true; do
	CON=$(ping -c 1 google.com | wc -l)
	if [ $CON -gt 0 ]; then 
		printf "Uploading...\n"
		python upload_manager.py
	else
		sleep 10
	fi
done


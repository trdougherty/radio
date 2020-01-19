source .env

while true; do
	ping -c1 google.com > /dev/null 2>&1
	if [ $? -eq 0 ]; then 
		printf "Uploading...\n"
		python upload_manager.py
	else
		sleep 10
	fi
done


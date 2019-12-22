source .env

# Make if there is no storage directory
mkdir -p ${STORAGE:="/mnt/storage"}

# Mounting the storage
mount ${STORAGE_NAME:="/dev/sda2"} $STORAGE
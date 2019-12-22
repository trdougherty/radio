source .env

# Gets user to modify permissions of mounted drive
USR=$(whoami)

# Make if there is no storage directory
mkdir -p ${STORAGE:="/mnt/storage"}

# Mounting the storage
mount -o uid=${USR},gid=${USR} ${STORAGE_NAME:="/dev/sda2"} ${STORAGE}

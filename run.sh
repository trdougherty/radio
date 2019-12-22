# Import Three-Finger Claw as TFC
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# Starts mounting process
source .env
bash mount_storage.sh 2> storage_error.txt

# Now it checks for the radio - if it exists

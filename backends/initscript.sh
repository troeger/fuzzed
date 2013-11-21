#! /bin/sh

### BEGIN INIT INFO
# Provides:          fuzzed-backend 
# Required-Start:    $local_fs $remote_fs
# Required-Stop:
# X-Start-Before:    
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: FuzzEd analysis backend
### END INIT INFO

THIS=/etc/init.d/fuzzed-backend
SCRIPTDIR=/usr/local/fuzzed-backend/

set -e

case "$1" in
  start)
        start-stop-daemon --start --background --name fuzzed-backend --exec /usr/bin/python --chdir $SCRIPTDIR --  daemon.py
        ;;
  stop)
        start-stop-daemon --stop --name fuzzed-backend
        ;;
  *)
        echo "Usage: $THIS {start|stop}" >&2
        exit 1
        ;;
esac

exit 0

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
SCRIPTDIR=/usr/local/fuzzed/FuzzEdBackend/
PIDFILE=/var/run/fuzzed.pid

set -e

case "$1" in
  start)
        start-stop-daemon --start --pidfile $PIDFILE --make-pidfile --background --exec /usr/bin/python --chdir $SCRIPTDIR --  daemon.py
        ;;
  stop)
        start-stop-daemon --stop --pidfile $PIDFILE --make-pidfile --retry=TERM/30/KILL/5
        ;;
  *)
        echo "Usage: $THIS {start|stop}" >&2
        exit 1
        ;;
esac

exit 0

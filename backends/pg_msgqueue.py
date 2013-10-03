'''
A small set of helper routines for performing message queueing
with PostgreSQL.
'''

import select, psycopg2, sys
import psycopg2.extensions

class PgMessageQueue():
    ''' A bidirectional message queue, based on PostgreSQL server notification.'''
    def __init__(self, hostname, dbname, username, passwd):
        self.conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s"%
                                     (hostname, dbname, username, passwd))
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

    def pull_message(self, channel):
        channel = channel.lower()       # PG channels are case insensitive
        self.cursor.execute("LISTEN %s;"%channel)
        while True:
            select.select([self.conn],[],[])
            self.conn.poll()
            while self.conn.notifies:
                notify = self.conn.notifies.pop()
                if notify.channel == channel:
                    self.cursor.execute("UNLISTEN %s;"%channel)
                    return (notify.pid, notify.payload)

    def push_message(self, channel, payload):
        channel = channel.lower()       # PG channels are case insensitive        
        self.cursor.execute("NOTIFY %s, '%s';"%(channel, payload))

# Simple test code, run it two times, were only one of them gets a command-line argument
if __name__ == '__main__':
    queue = PgMessageQueue('localhost', 'fuzztrees', 'fuzztrees', 'fuzztrees')
    if len(sys.argv) > 1:
        queue.push_message('requestChannel', 'myPayload')
        print queue.pull_message('responseChannel')
    else:
        print queue.pull_message('requestChannel')
        queue.push_message('responseChannel', 'myPayloadAnswer')


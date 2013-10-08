'''
A small set of helper routines for performing message queueing
with PostgreSQL.
'''

import select, psycopg2, sys, ConfigParser
import psycopg2.extensions

class PgMessageQueue():
    ''' A simple message queue system based on PostgreSQL server notification.
    '''
    def __init__(self, iniFile, recvChannels):
        ''' Constructs a new notification endpoint, DB settings are read from INI file.
            recvChannels can be a single string or a list of strings.
            The PostgreSQL LISTEN already happens here (and not in the pull method), 
            so that non-pulled messages for these channels are queued by the database.
            This allows a compute / pull cycle in the caller.
        '''
        # Connect to database
        config = ConfigParser.ConfigParser()
        config.read(iniFile)
        options=dict(config.items('all'))        
        self.conn = psycopg2.connect("host=%(db_host)s dbname=%(db_name)s user=%(db_user)s password=%(db_password)s"%options)
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()
        # Put channels into LISTEN mode for this node. PotsgreSQL channels are case-insensitive.
        if isinstance(recvChannels, str):
            self.channels = [recvChannels.lower(),]
        else:
            self.channels = [el.lower() for el in recvChannels]
        for channel in self.channels:
            self.cursor.execute("LISTEN %s;"%channel)

    def detach(self):
        ''' Detaches this node from notification messages.'''
        for channel in self.channels:
            self.cursor.execute("UNLISTEN %s;"%channel)  

    def pull_message(self):
        ''' Get a new message from the registered channel(s). Caller sleeps until receive.
            Returns the channel that got the message, the sender PID, and the payload.
        '''
        while True:
            select.select([self.conn],[],[])
            self.conn.poll()
            while self.conn.notifies:
                notify = self.conn.notifies.pop()
                if notify.channel in self.channels:
                    return {'channel': notify.channel, 'payload': notify.payload}

    def push_message(self, channel, payload):
        ''' Puts a message with the specified payload into the specified channel.
            Standard Postgres semantics apply, so if a listener does not pull a messages, than
            it is queued by the database.
        '''
        # PG channels are case insensitive        
        self.cursor.execute("NOTIFY %s, '%s';"%(channel.lower(), payload))

# Simple test code; run it two times, were only one of them gets a command-line argument
if __name__ == '__main__':
    queue = PgMessageQueue('database.ini', ('Channel1','Channel2'))
    if len(sys.argv) > 1:
        queue.push_message('Channel1', 'myPayload')
        print queue.pull_message()
    else:
        print queue.pull_message()
        queue.push_message('Channel2', 'myPayloadAnswer')


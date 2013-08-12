from subprocess import Popen, PIPE, signal
import os, sys

def shutdown(sig, func=None):
    print "Shutting down beanstalk connection ..."
    b.close()    

# Register cleanup code for termination
signal.signal(signal.SIGTERM, shutdown)

try:
	import beanstalkc
except:
	print "ERROR: Could not find beanstalk"
	exit(-1)

HOST = '127.0.0.1'
PORT = 11300

print "Starting beanstalkd messaging server ..."
beanstalk = Popen(["beanstalkd", "-l", HOST, "-p", str(PORT)])
if beanstalk.returncode != None:
	print "ERROR: %u while starting beanstalkd"%beanstalk.returncode
	exit(-1)
else:
	print beanstalk.pid
	print "...done."

#line = sys.stdin.readline()

try:
	b = beanstalkc.Connection(host=HOST, port=PORT, parse_yaml=False)
	#b = beanstalkc.Connection()
except beanstalkc.SocketError, exc:
	beanstalk.terminate()
	print "ERROR: Could not init Beanstalk Connection due to SocketError: %s"%exc
	exit(-1)

testfile = '''<?xml version="1.0" encoding="UTF-8"?>
<ft:FuzzTree xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ft="net.fuzztree" id="foo">
  <topEvent id="1" name="Server Failure" missionTime="1">
    <children xsi:type="ft:And" id="2">
      <children xsi:type="ft:BasicEventSet" id="3" name="Component Failure" quantity="3">
          <probability xsi:type="ft:CrispProbability" value="0.0001"/>
       </children>
    </children>
  </topEvent>
</ft:FuzzTree>
'''

b.use("configuration")
b.watch("configurationResults")

config = Popen(["ftconfiguration_exe.exe"])
if config.returncode != None:
	print "ERROR:  %u while starting config server" % config.returncode
	beanstalk.terminate()
	exit(-1)

while True:
	print "Press any key for status information, or 'q' for quitting ..."
	line = sys.stdin.readline()
	if line.startswith('q'):
		config.terminate()
		beanstalk.terminate()
		exit(0)
	elif line.startswith('p'):
		jobId = b.put(testfile)
		answer = b.reserve(timeout=0)
		print answer
	print b.stats()
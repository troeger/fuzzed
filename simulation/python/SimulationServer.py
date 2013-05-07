from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import TCPServer
from ctypes import *
import logging
import os

HOST = "localhost"
PORT = 8000
SIMULATION_LIBRARY = "ftsimulation" #"libftsimulation.so"

class ServerHandler(SimpleHTTPRequestHandler):

    filePath = "tree.faulttree"
    #TODO those need to be configurable
    missionTime = 1000
    numRounds = 100000
    cThresh = 0.00001
    maxTime = 10000

    resultFile = "tree.xml"
    
    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        print("received POST")
        if not self.headers["Content-type"] == "application/xml":
            self.send_response(404)
        data = self.rfile.read(int(self.headers["Content-length"]))
        file = open(self.filePath, "wb")
        try:
            file.write(data)
        finally:
            file.close()
        success = self.runSimulation()
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        if success:
            result = open(self.resultFile, "rb")
            self.wfile.write(result.read())
            result.close()
        else:
            self.wfile.write(bytes("not successful", "UTF-8"))

    def runSimulation(self):
        try:
            simLib = cdll.LoadLibrary(SIMULATION_LIBRARY)
            strbuf = create_string_buffer(self.filePath.encode('utf-8'))
            simLib.runSimulation(strbuf, self.missionTime, self.numRounds, c_double(self.cThresh), self.maxTime)
            fileName = os.path.splitext(self.filePath)[0]
            self.resultFile = fileName+ ".xml"
            return True
        except Exception as e:
            print("Error in simulation library call.")
            print(e)
            return False
    
def main():
    try:
        Handler = ServerHandler
        httpd = TCPServer((HOST, PORT), Handler)
        print("hello from simulation server, serving at port", PORT)
        httpd.serve_forever()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

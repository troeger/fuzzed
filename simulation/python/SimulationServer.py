from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.server
import socketserver
import logging

from ctypes import *

HOST = "localhost"
PORT = 8000
SIMULATION_LIBRARY = "ftsimulation" #"libftsimulation.so"

class ServerHandler(SimpleHTTPRequestHandler):

    filePath = "tree.xml"
    #TODO those need to be configurable
    missionTime = 1000
    numRounds = 100000
    cThresh = 0.00001
    maxTime = 10000

    resultFile = None
    
    def do_GET(self):
        #logging.error(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        #logging.error(self.headers)
        print("received POST")
        if not self.headers["content-type"] == "application/xml":
            self.send_response(404)
        data = self.rfile.read(int(self.headers["content-length"]))
        file = open("tree.xml", "wb")
        try:
            file.write(data)
        finally:
            file.close()
        success = self.runSimulation()
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        if success:
            self.wfile.write(resultFile.read())
        else:
            self.wfile.write(bytes("not successful", "UTF-8"))

    def runSimulation(self):
        try:
            simLib = cdll.LoadLibrary(SIMULATION_LIBRARY)
            simLib.runSimulation(self.filePath, self.missionTime, self.numRounds, self.cThresh, self.maxTime)
            return True
        except Exception as e:
            print("Error in simulation library call.")
            print(e)
            return False
    
def main():
    try:
        Handler = ServerHandler
        httpd = socketserver.TCPServer((HOST, PORT), Handler)
        print("hello from simulation server, serving at port", PORT)
        httpd.serve_forever()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

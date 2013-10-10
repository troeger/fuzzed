#!/bin/sh
/usr/bin/env python renderServer.py
echo $! > /var/run/fuzzTreeRendering.pid

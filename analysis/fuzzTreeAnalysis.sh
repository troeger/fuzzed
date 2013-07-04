#!/bin/sh
BASEDIR=$(dirname $0)
java -Djava.util.logging.config.file=$BASEDIR/jar/logging.properties  -jar $BASEDIR/jar/fuzzTreeAnalysis.jar   -runServer &
echo $! > /var/run/fuzzTreeAnalysis.pid


#!/bin/bash

if [ $# -eq 1 ]; then
	PAGES=$1; shift
else
	echo "<PAGES>"
	exit -1
fi

NAME="indeed"
LOG_FILE="$NAME.log"
#rm $LOG_FILE; scrapy crawl ctrip-reviews --logfile=${LOG_FILE}

OUTPUT="$NAME.jsonlines"

rm $OUTPUT $LOG_FILE
rm $OUTPUT; scrapy crawl "indeed" --output=${OUTPUT} --logfile=${LOG_FILE} -a PAGES=$PAGES

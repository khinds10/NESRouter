#!/usr/bin/env python
import time, json, datetime, os, re
print "Content-type: text/json\n\n"

# open the leases file
with open('/home/pi/logging/trafficSummary.log') as trafficSummaryFile: 
    trafficSummaryContent = trafficSummaryFile.read()
    trafficSummaryContent = trafficSummaryContent.split('\n')
    trafficSummaryContent = trafficSummaryContent[0].split('|')
       
print json.dumps(trafficSummaryContent)
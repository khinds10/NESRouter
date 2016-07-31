#!/usr/bin/env python
import time, psycopg2, json, datetime, os, re, commands

# setup postgresql connection
postgresConn = psycopg2.connect(database="network_stats", user="pi", password="password", host="127.0.0.1", port="5432")

# get traffic info as JSON
dBCursor = postgresConn.cursor()
    
# get current outside world IP Address
ipAddress = commands.getstatusoutput("ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1")
ipAddress = ipAddress[1].split('\n')
ipAddress = ipAddress[0]

# get readable uptime
uptime = commands.getstatusoutput("uptime -p")
uptime = uptime[1]
uptime = uptime.replace("up ", "")

# get total upload and dowload statistics [RX stand for received (download) and TX for tranferred (upload)]
ifconfig = commands.getstatusoutput("ifconfig")
ifconfig = ifconfig[1]
totalDownload = '';
totalUpload = '';
for line in ifconfig.splitlines():
    if 'RX bytes:' in line:
        try:
        
            # get the raw download bytes
            rawBytes = re.search('RX bytes:[0-9]+', line)
            rawDownLoadBytes = rawBytes.group(0)
            rawDownLoadBytes = rawDownLoadBytes.replace("RX bytes:", "").replace(" ", "")

            # get the raw upload bytes
            rawBytes = re.search('TX bytes:[0-9]+', line)
            rawUploadBytes = rawBytes.group(0)
            rawUploadBytes = rawUploadBytes.replace("TX bytes:", "").replace(" ", "")         
            
            # get human readable download stats
            readable = re.search('\([0-9a-zA-Z\. ]+\)', line)
            totalDownload = readable.group(0)
            totalDownload = totalDownload.replace("(", "")
            totalDownload = totalDownload.replace(")", "")
            
            # get human readable download stats
            readable = re.search('\([0-9a-zA-Z\. ]+\)$', line)
            totalUpload = readable.group(0)
            totalUpload = totalUpload.replace("(", "")
            totalUpload = totalUpload.replace(")", "")
        except:
            pass
        break

# get 1 / 7 / 30 day averages for internet usage
totalTrafficBytes = int(rawDownLoadBytes) + int(rawUploadBytes)

# get uptime in seconds (1st number is system up / 2nd is now time spend idle)
uptimeSeconds = commands.getstatusoutput("cat /proc/uptime")
uptimeSeconds = uptimeSeconds[1].split(' ')
uptimeSeconds = uptimeSeconds[0]

# calculate projected usage
avgUsagePerSecond = float(totalTrafficBytes)/float(uptimeSeconds)
oneDayTotals = int(avgUsagePerSecond) * 60 * 60 * 24
sevenDayTotals = oneDayTotals * 7
thirtyDayTotals = oneDayTotals * 30

# save to simple log file for reading by other devices / webpages
file_ = open('/home/pi/logging/trafficSummary.log', 'w')
file_.write(str(ipAddress) + '|' + str(uptime)  + '|' +  str(totalDownload)  + '|' +  str(totalUpload)  + '|' +  str(oneDayTotals)  + '|' +  str(sevenDayTotals)  + '|' +  str(thirtyDayTotals))
file_.close()

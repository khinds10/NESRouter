#!/usr/bin/env python
import time, json, datetime, os, re
print "Content-type: text/json\n\n"

# open the leases file
with open('/var/lib/misc/dnsmasq.leases') as leasesFile: 
    leasesFileContent = leasesFile.read()
    leasesFileContent = leasesFileContent.split('\n')
    
# for each line get the lease in question for the JSON response
leaseResponseInfo = []
for leaseFileLine in leasesFileContent:
    leaseFileLineInfo = leaseFileLine.split(' ') 
    try: 
        deviceInfo = []
        deviceInfo.append(leaseFileLineInfo[1])
        deviceInfo.append(leaseFileLineInfo[2])
        deviceInfo.append(leaseFileLineInfo[3])
        leaseResponseInfo.append(deviceInfo)
    except:
        pass

print json.dumps(leaseResponseInfo)
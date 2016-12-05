#!/usr/bin/env python
import time, commands, subprocess, re

# device and screen settings
ssid="NintendoWiFi"
displayIterations = 4
    
iteration = 0
while True:
    try:
        # cycle through the displays (3 for now)
        iteration = iteration + 1
        if (iteration > displayIterations):
            iteration = 1

        # get current outside world IP Address
        ipAddress = commands.getstatusoutput("ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1")
        ipAddress = ipAddress[1].split('\n')
        ipAddress = ipAddress[0]
        
        # get number of leases assigned
        leaseCount = commands.getstatusoutput("wc -l /var/lib/misc/dnsmasq.leases")
        leaseCount = leaseCount[1].split(' ')
        leaseCount = leaseCount[0]
        
        # get local computer network stats from ifstat command
        networkInfo = str(subprocess.check_output(['ifstat', '1', '1']))
        networkInfo = networkInfo.replace("eth1", "")
        networkInfo = networkInfo.replace("eth0", "")
        networkInfo = networkInfo.replace("wlan0", "")
        networkInfo = networkInfo.replace("KB/s in", "")
        networkInfo = networkInfo.replace("KB/s out", "")
        networkInfo = networkInfo.split()
        kbpsOut = networkInfo[0]
        kbpsIn = networkInfo[1]
      
        # get readable uptime
        uptime = commands.getstatusoutput("uptime -p")
        uptime = uptime[1]
        uptime = uptime.replace("up ", "")
        uptime = uptime.replace("days", "d")
        uptime = uptime.replace("hours", "h")
        uptime = uptime.replace("minutes", "m")        
        uptime = uptime.replace(", ", "-")
        uptime = uptime.replace(" ", "")
        uptime = uptime

        # get total upload and dowload statistics [RX stand for received (download) and TX for tranferred (upload)]
        ifconfig = commands.getstatusoutput("/sbin/ifconfig")
        ifconfig = ifconfig[1]
        downloadStats = '';
        uploadStats = '';
        for line in ifconfig.splitlines():
            if 'RX bytes:' in line:
                try:
                    m = re.search('\([0-9a-zA-Z\. ]+\)', line)
                    downloadStats = m.group(0)
                    downloadStats = downloadStats.replace("(", "")
                    downloadStats = downloadStats.replace(")", "")
                    m = re.search('\([0-9a-zA-Z\. ]+\)$', line)
                    uploadStats = m.group(0)
                    uploadStats = uploadStats.replace("(", "")
                    uploadStats = uploadStats.replace(")", "")
                except:
                    pass
                break

        # from the most recent summary file get the traffic summary for display
        summaryFile = open('/home/pi/logging/trafficSummary.log', 'r')
        trafficSummary = summaryFile.readline()
        trafficSummary = trafficSummary.split('|')

        # calculate projected internet usage for 1 / 7 and 30 days time
        oneDayTotalsUnit = " GiB"
        oneDayTotals = float(int(trafficSummary[4])/1000/1000/1000)
        if oneDayTotals < 1:
            oneDayTotals = float(int(trafficSummary[4])/1000/1000)
            oneDayTotalsUnit = " MiB"

        sevenDayTotals = float(int(trafficSummary[5])/1000/1000/1000)
        if sevenDayTotals < 1:
            sevenDayTotals = "--"

        thirtyDayTotals = float(int(trafficSummary[6])/1000/1000/1000)
        if thirtyDayTotals < 1:
            sevenDayTotals = "--"

        subprocess.call(["./digole", "clear"])
                
        subprocess.call(["./digole", "setColor", "11"])
        subprocess.call(["./digole", "printxy_abs", "0", "90", 'KEVIN'])
        
        subprocess.call(["./digole", "setColor", "255"])
        subprocess.call(["./digole", "printxy_abs", "0", "105", 'KEVIN'])
        subprocess.call(["./digole", "printxy_abs", "0", "120", 'KEVIN'])

        subprocess.call(["./digole", "BlasterMaster"]) #1
        subprocess.call(["./digole", "Castlevania"]) #0
        subprocess.call(["./digole", "ChipDale"]) #1 
        subprocess.call(["./digole", "Contra"]) #0
        subprocess.call(["./digole", "DuckTales"]) #0
        subprocess.call(["./digole", "Galaga"]) #1
        subprocess.call(["./digole", "GhostBusters"]) #1
        subprocess.call(["./digole", "Gradius"]) #0
        subprocess.call(["./digole", "KidIcarus"]) #1 
        subprocess.call(["./digole", "MarbleMadness"]) #1
        subprocess.call(["./digole", "MegaMan"]) #0
        subprocess.call(["./digole", "MetalGear"]) #0
        subprocess.call(["./digole", "Metroid"]) #1
        subprocess.call(["./digole", "PunchOut"]) #0 
        subprocess.call(["./digole", "SuperMario2"]) #1 
        subprocess.call(["./digole", "SuperMario3"]) #1
        subprocess.call(["./digole", "TMNT2"]) #0
        subprocess.call(["./digole", "TopGun"]) #0
        subprocess.call(["./digole", "Turtles"]) #1
        subprocess.call(["./digole", "Zelda"]) #1

        #if (iteration == 1):
        #    drawTextOnLine(1, str(ssid), titleFont, draw)
        #    drawTextOnLine(2, str(ipAddress), bodyFont, draw)
        #    drawTextOnLine(3, 'Up ' + str(kbpsIn), bodyFont, draw)
        #    drawTextOnLine(4, 'Down ' + str(kbpsOut), bodyFont, draw)
        #if (iteration == 2):
         #   drawTextOnLine(1, str(ssid), titleFont, draw)
         #   drawTextOnLine(2, "Leases " + str(leaseCount), bodyFont, draw)
         #   drawTextOnLine(3, '7d ' + str(sevenDayTotals) + " GiB", bodyFont, draw)
         #   drawTextOnLine(4, '30d ' + str(thirtyDayTotals) + " GiB", bodyFont, draw)
        #if (iteration == 3):
        #    drawTextOnLine(1, str(ssid), titleFont, draw)
        #    drawTextOnLine(2, str(ipAddress), bodyFont, draw)
        #    drawTextOnLine(3, '1d ' + str(oneDayTotals) + oneDayTotalsUnit, bodyFont, draw)
        #    drawTextOnLine(4, str(kbpsIn) + '/' + str(kbpsOut), bodyFont, draw)
        #if (iteration == 4):
        #    drawTextOnLine(1, str(ssid), titleFont, draw)
        #    drawTextOnLine(2, str(uptime), bodyFont, draw)
        #    drawTextOnLine(3, "RX " + str(downloadStats), bodyFont, draw)
        #    drawTextOnLine(4, "TX " + str(uploadStats), bodyFont, draw)
                
    except:
        pass
        
    time.sleep(10)
#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re
from random import randint

def randomTitleScreen(titleScreenNumber):
    '''show NES game title screen on the Digole Display
    @titleScreenNumber : number 1 to 20 of which title screen to show
    '''
    subprocess.call(["/home/pi/display/digole", "clear"])
    if titleScreenNumber == 1:
        subprocess.call(["/home/pi/display/digole", "BlasterMaster"])
    if titleScreenNumber == 2:
        subprocess.call(["/home/pi/display/digole", "Castlevania"])
    if titleScreenNumber == 3:
        subprocess.call(["/home/pi/display/digole", "ChipDale"]) 
    if titleScreenNumber == 4:
        subprocess.call(["/home/pi/display/digole", "Contra"])
    if titleScreenNumber == 5:
        subprocess.call(["/home/pi/display/digole", "DuckTales"])
    if titleScreenNumber == 6:
        subprocess.call(["/home/pi/display/digole", "Galaga"])
    if titleScreenNumber == 7:
        subprocess.call(["/home/pi/display/digole", "GhostBusters"])
    if titleScreenNumber == 8:
        subprocess.call(["/home/pi/display/digole", "Gradius"])
    if titleScreenNumber == 9:
        subprocess.call(["/home/pi/display/digole", "KidIcarus"]) 
    if titleScreenNumber == 10:
        subprocess.call(["/home/pi/display/digole", "MarbleMadness"])
    if titleScreenNumber == 11:
        subprocess.call(["/home/pi/display/digole", "MegaMan"])
    if titleScreenNumber == 12:
        subprocess.call(["/home/pi/display/digole", "MetalGear"])
    if titleScreenNumber == 13:
        subprocess.call(["/home/pi/display/digole", "Metroid"])
    if titleScreenNumber == 14:
        subprocess.call(["/home/pi/display/digole", "PunchOut"]) 
    if titleScreenNumber == 15:
        subprocess.call(["/home/pi/display/digole", "SuperMario2"]) 
    if titleScreenNumber == 16:
        subprocess.call(["/home/pi/display/digole", "SuperMario3"])
    if titleScreenNumber == 17:
        subprocess.call(["/home/pi/display/digole", "TMNT2"])
    if titleScreenNumber == 18:
        subprocess.call(["/home/pi/display/digole", "TopGun"])
    if titleScreenNumber == 19:
        subprocess.call(["/home/pi/display/digole", "Turtles"])
    if titleScreenNumber == 20:
        subprocess.call(["/home/pi/display/digole", "Zelda"])

def clearText():
    '''produce black background for text'''
    subprocess.call(["/home/pi/display/digole", "setFont", "18"])
    subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "98", "               "])
    subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "110", "               "])
    subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "120", "               "])
    subprocess.call(["/home/pi/display/digole", "setFont", "10"])
    
# device and screen settings
ssid="NintendoWiFi"
displayIterations = 4
subprocess.call(["/home/pi/display/digole", "clear"])
subprocess.call(["/home/pi/display/digole", "setColor", "255"])
randomTitleScreen(randint(1,20))

# begin the loop
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

        if iteration == displayIterations:
            randomTitleScreen(randint(1,20))
            
        clearText()
        if (iteration == 1):
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "100", str(ipAddress)])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "110", "Up " + str(kbpsIn) + ' kb'])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "120", "Down " + str(kbpsOut) + ' kb'])
            
        if (iteration == 2):
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "100", "Leases " + str(leaseCount)])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "110", "7d " + str(sevenDayTotals) + " GiB"])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "120", "30d " + str(thirtyDayTotals) + " GiB"])
            
        if (iteration == 3):            
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "100", str(ipAddress)])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "110", '1d ' + str(oneDayTotals) + oneDayTotalsUnit])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "120", str(kbpsIn) + '/' + str(kbpsOut)])
            
        if (iteration == 4):            
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "100", str(uptime)])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "110", "RX " + str(downloadStats)])
            subprocess.call(["/home/pi/display/digole", "printxy_abs", "0", "120", "TX " + str(uploadStats)])
    except:
        time.sleep(10)
    time.sleep(10)

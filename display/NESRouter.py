#!/usr/bin/env python
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
import time, commands, subprocess, re

# define fonts
font = ImageFont.load_default()
titleFont = ImageFont.truetype('/home/pi/display/8bit.ttf', 11)
bodyFont = ImageFont.truetype('/home/pi/display/8bit.ttf', 9)

# device and screen settings
device = ssd1306(port=1, address=0x3C)
ssid="NintendoWiFi"
displayIterations = 4

def drawTextOnLine(line, text, font, draw):
    """for given line and text and font, draw the text on the screen"""
    xAxis = 0
    yAxis = 16 * (line-1)
    draw.text((xAxis, yAxis), str(text), font=font, fill=255)
    pass
    
print 'NESRouter display has started...'
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

        #depending on which iteration screen we're on, show 1 of the 3 screens available 
        with canvas(device) as draw:
            if (iteration == 1):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, str(ipAddress), bodyFont, draw)
                drawTextOnLine(3, 'Up ' + str(kbpsIn), bodyFont, draw)
                drawTextOnLine(4, 'Down ' + str(kbpsOut), bodyFont, draw)
            if (iteration == 2):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, "Leases " + str(leaseCount), bodyFont, draw)
                drawTextOnLine(3, '7d ' + str(sevenDayTotals) + " GiB", bodyFont, draw)
                drawTextOnLine(4, '30d ' + str(thirtyDayTotals) + " GiB", bodyFont, draw)
            if (iteration == 3):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, str(ipAddress), bodyFont, draw)
                drawTextOnLine(3, '1d ' + str(oneDayTotals) + oneDayTotalsUnit, bodyFont, draw)
                drawTextOnLine(4, str(kbpsIn) + '/' + str(kbpsOut), bodyFont, draw)
            if (iteration == 4):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, str(uptime), bodyFont, draw)
                drawTextOnLine(3, "RX " + str(downloadStats), bodyFont, draw)
                drawTextOnLine(4, "TX " + str(uploadStats), bodyFont, draw)
    except:
        pass
        
    time.sleep(1.5)

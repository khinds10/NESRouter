#!/usr/bin/env python
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
import time, commands, subprocess

# define fonts
font = ImageFont.load_default()
titleFont = ImageFont.truetype('/home/pi/display/8bit.ttf', 11)
bodyFont = ImageFont.truetype('/home/pi/display/8bit.ttf', 9)

# device and screen settings
device = ssd1306(port=1, address=0x3C)
ssid="NintendoWiFi"
displayIterations = 3

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
        ipAddress = commands.getstatusoutput("ip addr show br0 | grep inet | awk '{print $2}' | cut -d/ -f1")
        ipAddress = ipAddress[1].split('\n')
        ipAddress = ipAddress[0]

        # get local computer network stats from ifstat command
        networkInfo = str(subprocess.check_output(['ifstat', '1', '1']))
        networkInfo = networkInfo.replace("eth1", "")
        networkInfo = networkInfo.replace("eth0", "")
        networkInfo = networkInfo.replace("wlan0", "")
        networkInfo = networkInfo.replace("br0", "")
        networkInfo = networkInfo.replace("KB/s in", "")
        networkInfo = networkInfo.replace("KB/s out", "")
        networkInfo = networkInfo.split()
        kbpsOut = networkInfo[0]
        kbpsIn = networkInfo[1]
       
        #depending on which iteration screen we're on, show 1 of the 3 screens available 
        with canvas(device) as draw:
            if (iteration == 1):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, str(ipAddress), bodyFont, draw)
                drawTextOnLine(3, 'Up ' + str(kbpsIn), bodyFont, draw)
                drawTextOnLine(4, 'Down ' + str(kbpsOut), bodyFont, draw)
            if (iteration == 2):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, "Hosts X", bodyFont, draw)
                drawTextOnLine(3, '7d X.XXGb', bodyFont, draw)
                drawTextOnLine(4, '30d X.XXGb', bodyFont, draw)
            if (iteration == 3):
                drawTextOnLine(1, str(ssid), titleFont, draw)
                drawTextOnLine(2, "Uptime Xd", bodyFont, draw)
                drawTextOnLine(3, '1d Avg X.XGb', bodyFont, draw)
                drawTextOnLine(4, str(kbpsIn) + '/' + str(kbpsOut), bodyFont, draw)
    except:
        pass
        
    time.sleep(1.5)

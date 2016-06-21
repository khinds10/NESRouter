# NESRouter
##Using an Old Nintendo Entertainment system case, produce a highly functional home router using a RaspberryPI 3

####1) Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
> 
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> 
> $ `umount /dev/sdb1`
> 
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
> 
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
> 
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "NESRouter"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>`alias l='ls -lh'`
>`source ~/.bashrc`

Reboot your PI to get the latest changes

`reboot`

###2) Supplies needed

	(List of supplies needed with images)

###3) Creating the WiFi Access Point
**Please note, before this becomes a router we're plugging in the RaspberryPi to an existing network via its ethernet port to install the following packages**

`sudo apt-get update && sudo apt-get -y upgrade`

`sudo apt-get install dnsmasq hostapd vim`

`sudo vi /etc/dhcpcd.conf`

Add the following line:

    denyinterfaces wlan0

`sudo vi /etc/network/interfaces`

Edit the wlan0 section so that it looks like this:

    allow-hotplug wlan0
    iface wlan0 inet static
        address 172.24.1.1
        netmask 255.255.255.0
        network 172.24.1.0
        broadcast 172.24.1.255

Reload DHCP Server and bounce the configuration for eth0 and wlan0 connections

`sudo service dhcpcd restart`

`sudo ifdown eth0; sudo ifup wlan0`

####Configure HOSTAPD (Change ssid and wpa_passphrase to the values of your own choosing)

`sudo vi /etc/hostapd/hostapd.conf`

    # This is the name of the WiFi interface we configured above
    interface=wlan0

    # Use the nl80211 driver with the brcmfmac driver
    driver=nl80211

    # This is the name of the network
    ssid=NintendoWiFi

    # Use the 2.4GHz band
    hw_mode=g

    # Use channel 6
    channel=6

    # Enable 802.11n
    ieee80211n=1

    # Enable WMM
    wmm_enabled=1

    # Enable 40MHz channels with 20ns guard interval
    ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

    # Accept all MAC addresses
    macaddr_acl=0

    # Use WPA authentication
    auth_algs=1

    # Require clients to know the network name
    ignore_broadcast_ssid=0

    # Use WPA2
    wpa=2

    # Use a pre-shared key
    wpa_key_mgmt=WPA-PSK

    # The network passphrase
    wpa_passphrase=password

    # Use AES, instead of TKIP
    rsn_pairwise=CCMP

We can check if it's working at this stage by running (but doesn't have full internet connectivity yet):

`sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf`

`sudo vi /etc/default/hostapd`

Find the line 

    #DAEMON_CONF="" 
    
and replace it with 

    DAEMON_CONF="/etc/hostapd/hostapd.conf"

Configure DNSMASQ

`sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig`

`sudo vi /etc/dnsmasq.conf`

    interface=wlan0           # Use interface wlan0
    listen-address=172.24.1.1 # Explicitly specify the address to listen on
    bind-interfaces           # Bind to the interface to make sure we aren't sending things elsewhere
    server=8.8.8.8            # Forward DNS requests to Google DNS
    domain-needed             # Don't forward short names
    bogus-priv                # Never forward addresses in the non-routed address spaces.
    
    # Assign IP addresses between 172.24.1.100 and 172.24.1.250 with infinite lease time (for device usage stats)
    dhcp-range=172.24.1.100,172.24.1.250,infinite 

SET UP IPV4 FORWARDING

`sudo vi /etc/sysctl.conf`

[uncomment]
net.ipv4.ip_forward=1

Activate it immediately with
`sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`

`sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`

`sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT`

`sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT`

Save iptables settings for next reboot

`sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"`

Create ipv4 rules file (with new contents)

`sudo vi /lib/dhcpcd/dhcpcd-hooks/70-ipv4-nat`

    iptables-restore < /etc/iptables.ipv4.nat

Restart Services

`sudo service hostapd start`
`sudo service dnsmasq start`

`sudo reboot`

####Adding UFW Firewall

`sudo apt-get install ufw`

Allow port 22 for public use (for remote network access)

`sudo ufw allow 22`

Allow all ports on my local network

`sudo ufw allow from 172.24.1.0/24`

Allow web ports to everyone

`sudo ufw allow 80`

Allow secure web ports to everyone

`sudo ufw allow 443`

Enable UFW and check the status

`sudo ufw --force enable`

`sudo ufw status`

### Connecting the ssd1306 Display

    (diagram here)
    VCC is connected to 3v
    GND is ground
    SDA is SDA
    SCL is SCL

Download and install drivers

`sudo apt-get install i2c-tools python-smbus python-pip ifstat git python-imaging`
`git clone https://github.com/rm-hull/ssd1306.git`
`sudo pip install pillow`

Now you should see the device in your i2cdetect command

`i2cdetect -y 1`
*it should show up in the grid of text as 3c*

Install Python Drivers

`cd ssd1306/`

`sudo python setup.py install`

Now your display should be ready to run

`python examples/pi_logo.py`
*should show a RaspberryPI symbol on your display to confirm it's working*

##  Setup the display script to run at startup

`crontab -e`

Add this line

`@reboot sleep 60 && python /home/pi/display/NESRouter.py 2>&1 >> /home/pi/display/NESRouter-output.log`

Verify the display starts working on reboot

`sudo reboot`

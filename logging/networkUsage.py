#!/usr/bin/env python
# postgres install that uses memcache and logs to a table every minute the network throughput
import time, commands, subprocess, re, memcache, psycopg2

# setup memcache / postgresql connections
memcacheClient = memcache.Client([('127.0.0.1', 11211)])
postgresConn = psycopg2.connect(database="network_stats", user="pi", password="password", host="127.0.0.1", port="5432")

def resetCache():
    """reset the cache value back to zero for all interfaces"""
    memcacheClient.add('rxTxKbps',"0.0,0.0,0.0,0.0,0.0,0.0", 0)
    memcacheClient.set('rxTxKbps',"0.0,0.0,0.0,0.0,0.0,0.0", 0)
    
def saveMinuteOfTraffic():
    """save minute worth of traffic stats to the DB"""
    rxTxKbps = memcacheClient.get('rxTxKbps')
    dBCursor = postgresConn.cursor()
    dBCursor.execute("INSERT INTO traffic_per_minute (time, eth0_down, eth0_up, eth1_down, eth1_up, wan0_down, wan0_up) VALUES (now(), "+rxTxKbps+")")
    postgresConn.commit()

# begin the logging of network traffic for each minute
secondCount = 1
resetCache()
while True:

    # get current network usage from all interfaces on this device
    networkInfo = str(subprocess.check_output(['ifstat', '1', '1']))
    networkInfo = networkInfo.replace("eth1", "").replace("eth0", "").replace("wlan0", "").replace("KB/s in", "").replace("KB/s out", "").split()

    # get current traffic for up to this minute of time
    try:
        rxTxKbps = memcacheClient.get('rxTxKbps')
        rxTxKbps = rxTxKbps.split(',')
    except:
        rxTxKbps = "0.0,0.0,0.0,0.0,0.0,0.0"
        pass

    # for each interface get the added traffic usage
    #   from networkInfo and then apply it to the memcache value as an added value
    count = 0
    while (count < 6):
        newTraffic = float(networkInfo[count]) + float(rxTxKbps[count])
        rxTxKbps[count] = str(newTraffic)
        count = count + 1
    memcacheClient.set('rxTxKbps',','.join(rxTxKbps), 0)
    secondCount = secondCount + 1

    # each minute save the values to DB and reset the cache
    if secondCount > 60:
        saveMinuteOfTraffic()
        resetCache()
        secondCount = 1
    
    # wait for another second to gather traffic stats again
    time.sleep(1)

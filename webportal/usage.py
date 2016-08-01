#!/usr/bin/env python
import time, psycopg2, json, datetime, os, re
print "Content-type: text/json\n\n"

# setup postgresql connection
postgresConn = psycopg2.connect(database="network_stats", user="pi", password="password", host="127.0.0.1", port="5432")

# get traffic info as JSON
dBCursor = postgresConn.cursor()

# get the 1-hour / 3-hour / 6-hour / 12-hour / 1-day / 3-day / 7-day / 30-day from query string
interval = os.environ.get("QUERY_STRING", "?12-hour")
interval = interval.replace('-',' ')
interval = re.sub('[^0-9a-zA-Z\- ]+', '', interval)
if (interval == ''):
    interval = '1 day'
    
# get DB results and return them as JSON
dBCursor.execute("SELECT COUNT(*) FROM traffic_per_minute WHERE time >= ( NOW() - INTERVAL '" + interval + "' ) AND eth0_down > 500")
rows = dBCursor.fetchone()
print json.dumps(rows[0])
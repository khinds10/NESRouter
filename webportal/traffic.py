#!/usr/bin/env python
import time, psycopg2, json, datetime, os, re
print "Content-type: text/json\n\n"

class DateEncoder(json.JSONEncoder):
    """for psycopg2 convert all the date time types to simple timestamps for JSON RESTFul Responses"""
    def default(self, obj):
        if isinstance(obj, datetime.date):
            JSDate = int(time.mktime(obj.timetuple())) * 1000
            return JSDate
        return json.JSONEncoder.default(self, obj)

# setup postgresql connection
postgresConn = psycopg2.connect(database="network_stats", user="pi", password="password", host="127.0.0.1", port="5432")

# get traffic info as JSON
dBCursor = postgresConn.cursor()

# get the 1-hour / 3-hour / 6-hour / 12-hour / 1-day / 3-day / 7-day / 30-day from query string
interval = os.environ.get("QUERY_STRING", "No Query String in url")
interval = interval.replace('-',' ')
interval = re.sub('[^0-9a-zA-Z\- ]+', '', interval)
if (interval == ''):
    interval = '1 day'
    
# get DB results and return them as JSON (Note: 5 hours subtracted for my local timezone EST)
dBCursor.execute("SELECT time - INTERVAL '5 hour',eth0_down,eth0_up FROM traffic_per_minute WHERE time >= ( NOW() - INTERVAL '" + interval + "' )")
rows = dBCursor.fetchall()

# get averages for each 5 minutes as JSON results for the google report
results = []
date = '';
upload = 0.0;
download = 0.0;
x = 0
for row in rows:
    if x == 0:
       date = row[0]
    upload = upload + row[1]
    download = download + row[2]
    x = x + 1
    if x == 5:
        upload = upload/5
        download = download/5
        results.append([date, upload, download])
        x = 0

print json.dumps(results, cls=DateEncoder)
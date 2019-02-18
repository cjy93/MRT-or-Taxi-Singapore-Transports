from twisted.internet import reactor
import urllib.request
import json 
import datetime

taxiApiUrl = 'https://api.data.gov.sg/v1/transport/taxi-availability'

def getTaxiData():
    now = datetime.datetime.now()
    with urllib.request.urlopen(taxiApiUrl) as url:
        data = json.loads(url.read().decode())
        #print(data)
        print(data['features'][0]['properties']['timestamp'])

        #saving
        nowStr = now.strftime("%Y%m%d_%H%M%S_%s")
        fnToSaveTo = 'taxi_%s.json' % (nowStr,)
        print('Saving to %s\n' % fnToSaveTo)
        with open(fnToSaveTo, 'w+') as outfile:
            json.dump(data, outfile)

    reactor.callLater(60.0, getTaxiData) # start the rest 60s later

def f(s):
    print("this will run 3.5 seconds after it was scheduled: %s" % (s,))
    
    reactor.callLater(3.5, f, "hello, world")

#reactor.callLater(3.5, f, "hello, world")
reactor.callLater(10.0, getTaxiData) # start 1st run 10s later

# f() will only be called if the event loop is started.
reactor.run()

#getTaxiData()



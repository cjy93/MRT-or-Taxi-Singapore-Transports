# https://geocoder.api.here.com/6.2/geocode.json?app_id=CqnyNhJQRmXS5JggWAos&app_code=qsE9fGn1RRAPNOxzG1OeFA&searchtext=singapore%20woodlands

#https://stackoverflow.com/questions/35120250/python-3-get-and-parse-json-api
import os
import json
os.getcwd()
# pick one of the json file to open for debugging
#filename = "taxi_20190124_234520_1548344720.json"  # initialise and debugging
#fullpath = "taxiData_0/taxiData_0/{}".format(filename)

# make function to import json
def gettaxiDetails(fullpath):    
    fullpathSplit1 = fullpath.split("\\") # since \t in string is tab
    filename = fullpathSplit1[-1]
    #print(filename)
                                    
    with open(fullpath, 'r') as fp:
        obj = json.load(fp)
    # pretty print json
    # https://stackoverflow.com/questions/12943819/how-to-prettyprint-a-json-file
    #print(json.dumps(obj, indent=4, sort_keys=True))
    #print(obj)

    # Get the lat long coordinates
    longlat = obj['features'][0]['geometry']['coordinates']

    # Get the taxi_count
    taxiCount = (obj['features'][0]['properties']['taxi_count'])

    # Get the status
    taxiStatus = (obj['features'][0]['properties']['api_info']['status'])

    # Get the timestamp
    timeStampTaxi = obj['features'][0]['properties']['timestamp']
    #print(timeStampTaxi)
    split1Lta = timeStampTaxi.split("T")
    #print(split1Lta)
    split2Lta = split1Lta[1].split("+")
    #print(split2Lta)
    LtaTimestamp = split2Lta


    # Get the crawl for datetime within title
    firstSplit = filename.split("taxi_")
    #print(firstSplit)
    secondSplit = firstSplit[1].split(".json")
    #print(secondSplit)
    thirdSplit = secondSplit[0].split("_")
    #print(thirdSplit)

    # get the crawled dates
    crawlYY = thirdSplit[0][0:4]
    crawlMM = thirdSplit[0][4:6]
    crawlDD = thirdSplit[0][6:]
    #print(crawlDD)

    # Get the crawled time
    crawlhh = thirdSplit[1][0:2]
    crawlmin =  thirdSplit[1][2:4]
    crawlss = thirdSplit[1][4:]
    #print(crawlss)
    
    # convert datetime to 'YYYY-MM-DD HH:MM:SS'   
    crawlTime = '{}-{}-{} {}:{}:{}'.format(crawlYY,crawlMM,crawlDD,crawlhh,crawlmin,crawlss)
    LtaTimestamp = '{} {}'.format(split1Lta[0],LtaTimestamp[0])
    print(LtaTimestamp)
    taxidetailsDict = {'LtaTimestamp':LtaTimestamp,
                      'crawlTime':crawlTime,
                      'taxiCount':taxiCount,
                      'taxiStatus':taxiStatus,
                      'longlat':longlat}
    return(taxidetailsDict)

# call the function
#taxiDetailsFull = gettaxiDetails(fullpath)
#print(taxiDetailsFull)

# check if the same records are already in the table
import mysql.connector
from datetime import date, datetime
import sys
import pandas as pd

def checkSameRow(taxiDetailsFull):
    #user,pw, host,db = 'it8701ca2','password123','localhost','it8701ca2_taxi'

    #cnx = mysql.connector.MySQLConnection(user=user, password=pw, host=host, database=db)
    #cursor = cnx.cursor()

    select_stmt = ("SELECT COUNT(idtaxisummary) FROM taxisummary WHERE LtaTimestamp = %(LtaTimestamp)s;")

    LtataxidetailsDict = {'LtaTimestamp':taxiDetailsFull['LtaTimestamp']}

    cursorSQLCountInserted = 999 #error
    try:
        cursor.execute(select_stmt, LtataxidetailsDict)
        cursorSQL = cursor.fetchall()
        cursorSQLCountInserted = cursorSQL[0][0]
        #print(cursorSQL)
        #print(cursorSQLCountInserted)
        print("Query finished!")
        if cursorSQLCountInserted > 0:
            print("Repeated! {}".format(LtataxidetailsDict['LtaTimestamp']))

    except ValueError:
        print("Unexpected error:", sys.exc_info()[0])
        #exit()

    #finally:
    #    cursor.close()
    #    cnx.close()
    
    return(cursorSQLCountInserted)




# Insert the above into TaxiSummary Table in MYSQL
import mysql.connector,sys
from datetime import date, datetime

def insertSummaryTaxi(taxiDetailsFull,cursorSQLCountInserted):

    #user,pw, host,db = 'it8701ca2','password123','192.168.1.10','it8701ca2_taxi2'

    #cnx = mysql.connector.MySQLConnection(user=user, password=pw, host=host, database=db)
    #cursor = cnx.cursor()

    insert_stmt = ("INSERT INTO `taxisummary` (`LtaTimestamp`, `crawlTime`, `taxiCount`, `status`) "+
                   "VALUES (%(LtaTimestamp)s,%(crawlTime)s, %(taxiCount)s, %(taxiStatus)s);")

    subsettaxidetailsDict = {'LtaTimestamp':taxiDetailsFull['LtaTimestamp'],
                          'crawlTime':taxiDetailsFull['crawlTime'],
                          'taxiCount':taxiDetailsFull['taxiCount'],
                          'taxiStatus':taxiDetailsFull['taxiStatus'],
                           }

    # Make sure only 1 time each data is inserted
    if cursorSQLCountInserted == 0:

    # error catching
        try:
            cursor.execute(insert_stmt, subsettaxidetailsDict)
            cnx.commit()
            datasetId = cursor.lastrowid
            print("Insert done with id:{}!".format(datasetId))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            exit()

        #finally:
        #    cursor.close()
        #    cnx.close()
            
        return(datasetId)
            
        # the output goes into the MYSQL




# Insert data into the taxiDetails Table in MySQl
# Insert the above into TaxiSummary Table in MYSQL
import mysql.connector,sys
from datetime import date, datetime

def insertDetailsTaxi(taxiDetailsFull, cursorSQLCountInserted , datasetId):
    #user,pw, host,db = 'it8701ca2','password123','192.168.1.10','it8701ca2_taxi2'

    #cnx = mysql.connector.MySQLConnection(user=user, password=pw, host=host, database=db)
    #cursor = cnx.cursor()

    try:
    # loop through the list of longlat
        # make sure only insert once per dataset
        if cursorSQLCountInserted == 0:
            for row in taxiDetailsFull['longlat']:

                insert_stmt = ("INSERT INTO `taxidetails` (`lat`, `long`, `datasetId`)"+
                               " VALUES (%(lat)s, %(long)s, %(datasetId)s);")

                subsettaxidetailsDict2 = {'long':row[0], 'lat':row[1] , 'datasetId':datasetId } # thie datasetId is from summary


                cursor.execute(insert_stmt, subsettaxidetailsDict2)
                #cnx.commit()
                datasetIdDetailKey = cursor.lastrowid
                #print("Insert details done with id:{}!".format(datasetIdDetailKey))
            cnx.commit() # commit once per dataset, faster than commit once per row
    except:
        print("Unexpected error:", sys.exc_info())
        #exit()

    #finally:
    #    cursor.close()
    #    cnx.close()



import os
counter = 0

user,pw, host,db = 'it8701ca2','password123','localhost','it8701ca2_taxi'

cnx = mysql.connector.MySQLConnection(user=user, password=pw, host=host, database=db)
cursor = cnx.cursor()

# change date here for the 5 days manually
for root, dirs, files in os.walk("taxi_20190128"):
    files.sort() # sort by filename
    for file in files:         
        if file.endswith(".json"):
            counter = counter + 1
            print('current %s' % (file,))
            fullpath = os.path.join(root, file) # this inputs the fullpath of all the datasets
            taxiDetailsFull = gettaxiDetails(fullpath)
            cursorSQLCountInserted = checkSameRow(taxiDetailsFull)
            datasetId = insertSummaryTaxi(taxiDetailsFull,cursorSQLCountInserted)
            insertDetailsTaxi(taxiDetailsFull, cursorSQLCountInserted , datasetId)
cursor.close()
cnx.close()
            
print(counter)

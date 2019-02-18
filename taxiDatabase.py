"""
Extract relevant data from database
"""
import mysql.connector,sys
from datetime import date, datetime
import pandas as pd
from decimal import Decimal
import time
#import pymysql

#user,pw, host,dbSchema = 'it8701ca2','password123','192.168.1.10',\
#                         'it8701ca2_taxi2'


user,pw, host,dbSchema = 'it8701ca2','password123','127.0.0.1',\
                         'it8701ca2_taxi'

# 127.0.0.1 or localhost
class TaxiDatabase:
    def __init__(self):
        print("start")
        # class so we can mysql.connector.connect only one time which is faster
        self.cnx = mysql.connector.connect(
            user=user, password=pw, host=host, database=dbSchema)
        self.cursor = self.cnx.cursor(buffered=True)
    
    def genericSelect(self, selectSqlStatement, columnsList, data=None):
        select_stmt = (selectSqlStatement)
        try:
            if data is not None:
                self.cursor.execute(select_stmt, data)
            else:
                self.cursor.execute(select_stmt)
            fetchAll = self.cursor.fetchall()
            df = pd.DataFrame(fetchAll, columns = columnsList)
            return df
        except DeprecationWarning:
            print("Error:", __file__, sys.exc_info())
    
    
    def selectAllFromTaxiSummary(self):
        selectSqlStatement = 'SELECT `idtaxisummary`, `LtaTimestamp`, ' \
                         '`taxiCount`, `status` FROM ' \
                         'taxisummary '\
                         'ORDER BY `idtaxisummary`;'
        col = ['idtaxisummary', 'ltaTimestamp', 'taxiCount', 'status']
        return self.genericSelect(selectSqlStatement, col)
   
    def selectTaxiDetailsWhereDatasetId(self, datasetId):
        selectSqlStatement = 'SELECT idtaxidetails,lat,`long` ' \
                'FROM taxidetails ' \
                'WHERE datasetId = %(datasetId)s;'
        
        selectParm = {
                'datasetId': datasetId,
        }
        col = ['idtaxidetails', 'lat', 'long']
        return self.genericSelect(selectSqlStatement, col, selectParm)
        
        
    def selectBuildingDetailsFrPostal(self, postalCodes):
        selectSqlStatement = 'SELECT * FROM it8701ca2_taxi.postalcodes '\
                              'WHERE postalCode = %(postalcode)s  ;'
        
        selectParm = {
                'postalcode': postalCodes,
        }
        col = ['id', 'add', 'blk', 'bldg' , 'lat' , 'long' , 'postal']
        return self.genericSelect(selectSqlStatement, col, selectParm)
    
    def selectNearestTaxi(self, datasetId, lat, lon, radiusKm):
        selectSqlStatement = """SELECT
        idtaxidetails, lat, `long`, (
            6371 * acos (
            cos ( radians(%(lat)s) )
            * cos( radians( lat ) )
            * cos( radians( `long` ) - radians(%(lon)s) )
            + sin ( radians(%(lat)s) )
            * sin( radians( lat ) )
            )
        ) AS distance
        FROM taxidetails
        WHERE datasetId = %(datasetId)s
        HAVING distance < %(radiusKm)s  -- within xxkm
        ORDER BY distance
        -- LIMIT 0 , 20; -- limit to nearest 20 taxis
"""
        selectParm = {
            'lat': lat,
            'lon': lon,
            'radiusKm': radiusKm,
            'datasetId': datasetId
            }
        col = ['idtaxidetails', 'lat', 'long', 'distance']
        return self.genericSelect(selectSqlStatement, col, selectParm)
    
    
    def __del__(self):
        print('TaxiDatabase: __del__')
        self.cursor.close()
        self.cnx.close()

if __name__ == '__main__':
    db = TaxiDatabase()
    # run this taxidatabase as a standalone name rather than as a library. 
    # means when you import as a library, you dont want the whole script to run, but you can still use the functions
    #df = db.selectAllFromTaxiSummary()
    #for testing
    #print(df)

    df = db.selectNearestTaxi( 1, 1.3, 103.8, 2)
    print(df)
    numOfRecords = df.shape[0]
    print('num of records: {}'.format(numOfRecords))

    df = db.selectAllFromTaxiSummary()
    print(df)
    
    df1 = db.selectBuildingDetailsFrPostal("018925")
    print(df1)

    #db.closeDb()



import sqlite3
import dataClass
class AbsorbDatabase:
    def __init__(self,dbPath,routeID='',timestamp='',tripID=''):
        con = sqlite3.connect(dbPath)
        curs = con.cursor()
        if routeID=='':
            sqlData = curs.execute("select * from vehicle_feed") 
        elif routeID!='' and timestamp=='' :
            sqlData = curs.execute("select * from vehicle_feed where route_id =" + routeID) 
        else:
            sqlData = curs.execute("select * from vehicle_feed where route_id =" + routeID + " and timestamp = " + timestamp + " trip_id = " + tripID) 
            
        self.allData=[]
        while True:
            entry = dataClass.VehicleData()
            instance = sqlData.fetchone()
            if instance==None:
                break
            entry.setID(instance[0])
            entry.setLatitude(instance[1])
            entry.setLongitude(instance[2])
            entry.setRouteID(str(int(instance[4])))
            entry.setTripID(instance[5])
            entry.setTimeStamp(instance[6])
            self.allData.append(entry)
        
    def findWithSameRouteId(self,id):
        sameData=[]
        for i in self.allData:
            if i.getRouteID() == id:
                sameData.append(i)
        return sameData
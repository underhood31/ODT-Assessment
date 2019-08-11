class VehicleData:

    def setID(self,id):
        self.id=id
    
    def setLatitude(self,l):
        self.latitude = l
    
    def setLongitude(self,l):
        self.longitude = l
    
    def setRouteID(self,i):
        self.routeID = i

    def setTimeStamp(self,s):
        self.timeStamp = s
    
    def setTripID(self,s):
        self.tripID = s
        
    def getID(self):
        return self.id
    
    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude
    
    def getRouteID(self):
        return self.routeID

    def getTimeStamp(self):
        return self.timeStamp

    def getTripID(self):
        return self.tripID
        


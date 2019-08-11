from google.transit import gtfs_realtime_pb2
import requests
import dataClass
import absorbDatabase as ad
API_URL = "https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=aw6ZI9SDxE9a4chXMwmlRwMvPVvxG8Ad"
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(API_URL)
feed.ParseFromString(response.content)
allData = []
for entity in feed.entity:
    data = dataClass.VehicleData()
    data.setID(entity.vehicle.vehicle.id)
    data.setLatitude(entity.vehicle.position.latitude)
    data.setLongitude(entity.vehicle.position.longitude)
    data.setRouteID(entity.vehicle.trip.route_id)
    data.setTripID(entity.vehicle.trip.trip_id)
    data.setTimeStamp(entity.vehicle.timestamp)
    allData.append(data)

# print(allData[0].getTripID())
# id=allData[100].getRouteID()
# time = allData[100].getTimeStamp()
# tid = allData[100].getTripID()
# dbs = ad.AbsorbDatabase('bus_movements_2019_08_01.db',routeID=str(id),tripID=str(tid))
# print(dbs.findWithSameRouteId(str(id))[0].getRouteID())
# print(id)

for i in allData:
    print(i.getRouteID())
    print(i.getTripID())
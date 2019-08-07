from google.transit import gtfs_realtime_pb2
import requests
API_URL = "https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=aw6ZI9SDxE9a4chXMwmlRwMvPVvxG8Ad"
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(API_URL)
feed.ParseFromString(response.content)
data = {'vehicle_id':[],'vehicle_lat':[],'vehicle_lon':[],'vehicle_route_id':[],'vehicle_timestamp':[]}
for entity in feed.entity:
    data['vehicle_id'].append(entity.vehicle.vehicle.id) 
    data['vehicle_lat'].append(entity.vehicle.position.latitude)
    data['vehicle_lon'].append(entity.vehicle.position.longitude)
    data['vehicle_route_id'].append(entity.vehicle.trip.route_id)
    data['vehicle_timestamp'].append(entity.vehicle.timestamp)
    break

print(data)
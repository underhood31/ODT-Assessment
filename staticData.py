import pygtfs
import absorbDatabase
import sqlite3
import operator
import math

def findDistInKm(lat0, lng0, lat1, lng1):					#FUNCTION FROM www.github.com/google/transitfeed/examples
	"""
	Compute the geodesic distance in meters between two points on the
	surface of the Earth.  The latitude and longitude angles are in
	degrees.
	Approximate geodesic distance function (Haversine Formula) assuming
	a perfect sphere of radius 6367 km (see "What are some algorithms
	for calculating the distance between 2 points?" in the GIS Faq at
	http://www.census.gov/geo/www/faq-index.html).  The approximate
	radius is adequate for our needs here, but a more sophisticated
	geodesic function should be used if greater accuracy is required
	(see "When is it NOT okay to assume the Earth is a sphere?" in the
	same faq).
	"""
	deg2rad = math.pi / 180.0
	lat0 = lat0 * deg2rad
	lng0 = lng0 * deg2rad
	lat1 = lat1 * deg2rad
	lng1 = lng1 * deg2rad
	dlng = lng1 - lng0
	dlat = lat1 - lat0
	a = math.sin(dlat*0.5)
	b = math.sin(dlng*0.5)
	a = a * a + math.cos(lat0) * math.cos(lat1) * b * b
	c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
	return 6367000.0 * c
  

sched = pygtfs.Schedule(":memory:")                # create a schedule object (a sqlite database)
pygtfs.append_feed(sched, "GTFS.zip") 
routes = sched.routes

# Storing the static trip IDs
static_trip_ids=[]
for i in routes:
	x=i.trips.pop()
	static_trip_ids.append(int(x.id))
print(static_trip_ids[0])

#getting saved trip ids
saved_trip_ids=[]
con = sqlite3.connect("bus_movements_2019_08_01.db")
curs = con.cursor()
sqlData = curs.execute("select trip_id from vehicle_feed")
instance = sqlData.fetchall()
for i in instance:
	saved_trip_ids.append(int(i[0]))
print(saved_trip_ids[0])

#comparing trip ids in static vs saved and implementing algo
allCases=[]
for i in static_trip_ids:
	found=False
	for j in saved_trip_ids:
		if i==j:
			found=True
			break
	if found:
		this_case={}
		stopt = sched.stop_times
		stops=[]
		# Getting needed stop data
		for j in stopt:
			if int(j.trip_id)==i:
				stops.append(j)
		#sorting sort wrt stop_sequence
		stopt.sort(key=operator.attrgetter('stop_sequence'))
		for j in stops:
			#Getting static data
			static_time_hour=int(str(j.arrival_time).split(":")[0])
			static_time_min=int(str(j.arrival_time).split(":")[1])
			static_stop_id=j.stop_id
			static_lat=sched.stops_by_id("2101")[0].stop_lat
			static_long=sched.stops_by_id("2101")[0].stop_lon
			sqlData = curs.execute("select time,lat,lng from vehicle_feed where trip_id="+str(i))
			instance = sqlData.fetchall()
			for k in instance:
				if int(k[0].split(":")[0])==static_time_hour:
					minute=int(k[0].split(":")[1])
					if abs(minute-static_time_min)<=1:
						dist=findDistInKm(static_lat,static_long,float(k[1]),float(k[2]))
						this_case[static_stop_id]=dist
						break
		allCases.append(this_case)
						#getting saved data
			
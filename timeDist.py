import pygtfs
import absorbDatabase
import sqlite3
import operator
import math
import pickle
import datetime
def findDistInM(lat0, lng0, lat1, lng1):					#FUNCTION FROM www.github.com/google/transitfeed/examples
	"""
	Compute the geodesic distance in meters between two points on the
	surface of the Earth.  The latitude and longitude angles are in
	degrees.
	Approximate geodesic distance function (Haversine Formula) assuming
	a perfect sphere of radius 6367 M (see "What are some algorithms
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
  
def make_dict(name,db_path):
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
	con = sqlite3.connect(db_path)
	curs = con.cursor()
	sqlData = curs.execute("select trip_id from vehicle_feed")
	instance = sqlData.fetchall()
	
	for i in instance:
		try:
			saved_trip_ids.append(int(i[0]))
		except:
			continue
	print(saved_trip_ids[0])

	#comparing trip ids in static vs saved and implementing algo
	allCases={}
	m=0
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
				print(m)
				m+=1
				try:
					static_time=j.arrival_time
				except:
					continue
				static_stop_id=j.stop_id
				static_lat=sched.stops_by_id(static_stop_id)[0].stop_lat
				static_long=sched.stops_by_id(static_stop_id)[0].stop_lon
				sqlData = curs.execute("select time,lat,lng from vehicle_feed where trip_id="+str(i))
				instance = sqlData.fetchall()
				for k in instance:
					dist = findDistInM(static_lat,static_long,float(k[1]),float(k[2]))
					if dist<1000:
						minute=int(k[0].split(":")[1])
						hour=int(k[0].split(":")[0])
						real_time = datetime.timedelta(hours=hour,minutes=minute)
						this_case[static_stop_id]=int(abs(static_time-real_time).seconds/60);
						break
# if int(k[0].split(":")[0])==static_time_hour:
					# 	minute=int(k[0].split(":")[1])
					# 	if abs(minute-static_time_min)<=1:
					# 		dist=findDistInM(static_lat,static_long,float(k[1]),float(k[2]))
					# 		this_case[static_stop_id]=dist
					# 		break
			if this_case!={}:
				allCases[i]=this_case
							#getting saved data
	with open(name + '.dictionary', 'wb') as config_dictionary_file:
		pickle.dump(allCases, config_dictionary_file)


make_dict('timeDist1','bus_movements_2019_08_01.db')
make_dict('timeDist2','bus_movements_2019_08_02.db')
# make_dict('timeDist3','bus_movements_2019_08_03.db')
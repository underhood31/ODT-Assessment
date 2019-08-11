# import pygtfs
# import absorbDatabase
# import sqlite3
# import operator
# sched = pygtfs.Schedule(":memory:")                # create a schedule object (a sqlite database)
# pygtfs.append_feed(sched, "GTFS.zip") 
# stopt = sched.stop_times


# print("stopt[0].arrival_time",stopt[0].arrival_time)
# print(type(stopt[0].arrival_time))
# print("stopt[0].stop_id",stopt[0].stop_id)
# print(type(stopt[0].stop_id))
# print("stopt[0].stop_sequence", stopt[0].stop_sequence)
# print(type(stopt[0].stop_sequence))
# print("timepoint",stopt[0].timepoint)
# print(type(stopt[0].timepoint))
# print("trip_id",stopt[0].trip_id)
# print(type(stopt[0].trip_id))

# stopt.sort(key=operator.attrgetter('stop_sequence'))


# # Storing the static trip IDs
# # static_trip_ids=[]
# # for i in routes:
# # 	x=i.trips.pop()
# # 	static_trip_ids.append(int(x.id))
# # print(static_trip_ids[0])

import psutil
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.write_image('figure.png')

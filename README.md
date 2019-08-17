# ODT-Assessment
## Report on analysis of the schedule followed by the buses and their actual defined schedules.
## Instructions to use ### (Python3)
### Add the database of August 1, 2, 3 with the name bus_movements_2019_08_01.db, bus_movements_2019_08_02.db, bus_movements_2019_08_03.db in the root folder
### Run script staticData.py(This might take upto 2 hours)
#### It will create dictionaries trip_dist_diff1, trip_dist_diff2, trip_dist_diff3, from data of day 1,2 and 3 in the format {trip_id:{stop_id:distance from planned positions(m) ...}
### Run script timeDist.py(This might also take upto 2 hours)
#### It will create dictionaries timeDist1, timeDist2, timeDist3, from data of day 1,2 and 3 in the format {trip_id:{stop_id:time difference between planned and actual time at a stop ...}
### Run scipt Webapp.py 
#### it will open a local Webapp, open that page in browser, at the bottom of the page you will get an option to download Report.pdf based on the data

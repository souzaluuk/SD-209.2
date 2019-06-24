import math
import matplotlib.pyplot as plt
import pandas as pd
import time

import utils
import Entidades

tripFields = [
	'starttime',
	'stoptime',
	'bikeid',
	'tripduration',
	'from_station_id',
	'to_station_id'
	]

stationFields = [
	'station_id',
	'current_dockcount'
	]

trip = pd.read_csv('data/trip.csv', sep =',', names=tripFields) # read data trips
station = pd.read_csv('data/station.csv', sep =',', names=stationFields) # read data stations

# startTimes = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip.starttime.values ] # get all starttimes in timestemp
# startTimesMin = min(startTimes)
# startTimes = [ value-startTimesMin for value in startTimes ] # normalize time
# startTimesSorted = sorted(startTimes) # sorted important
# inliers = utils.noOutliers(startTimesSorted) # get inliers

# k = round(1+3.3*math.log10(len(inliers))) ; print('K:',k)# classes
# h = (max(inliers)-min(inliers))/k ; print('H:',h) # intervals

# plt.hist(inliers,bins=k)
# # plt.plot(inliers,'o')
# plt.show()

tripDurations = [ float(sec.replace('.','')) for sec in  trip.tripduration.values ] # get all tripduration in sec
tripDurationMin = min(tripDurations)
tripDurations = [ value-tripDurationMin for value in tripDurations ] # normalize time
tripDurationsSorted = sorted(tripDurations) # sorted important
inliers = utils.noOutliers(tripDurationsSorted) # get inliers

k = round(1+3.3*math.log10(len(inliers))) ; print('K:',k)# classes
h = (max(inliers)-min(inliers))/k ; print('H:',h) # intervals

print('total:',len(tripDurationsSorted),'inliers:',len(inliers))

plt.hist(inliers,bins=k)
# plt.plot(inliers,'o')
plt.show()

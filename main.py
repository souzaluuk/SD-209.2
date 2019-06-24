import pandas as pd

import utils

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
# utils.plotHistogram(startTimes,'Tempos de ínicio')

tripDurations = [ float(sec.replace('.','')) for sec in  trip.tripduration.values ] # get all tripduration in sec
utils.plotHistogram(tripDurations,'Tempo de Viagens')

# stopTime = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip.stoptime.values ] # get all stoptimes in timestemp
# utils.plotHistogram(stopTime,'Tempos de fim')
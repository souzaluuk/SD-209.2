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
	'install_dockcount'
	]

trip = pd.read_csv('data/trip.csv', sep =',', names=tripFields)[:25000] # read data trips
station = pd.read_csv('data/station.csv', sep =',', names=stationFields) # read data stations

tripDurations = [ float(milisec.replace('.','')) for milisec in  trip.tripduration.values ] # get all tripduration in milisec
utils.plotHistogram(tripDurations,'Tempo de Viagens')

# dictStations = { name:{'bikes':0, 'docks':count,'docksAvailable':count} for name,count in station.values }

# bikeIds = set(trip.bikeid)

# for registry in trip.values:
# 	rmBike = registry[2] # bikeid 
# 	fromStationId = registry[5] # station_id
# 	if rmBike in bikeIds:
# 		bikeIds.remove(rmBike)
# 		dictStations[fromStationId]['bikes'] += 1
# 		dictStations[fromStationId]['docksAvailable'] -= 1

# for key in dictStations:
# 	print(key,dictStations[key])

# for registry in trip[:10].values:
# 	print(registry)
# 	rmDock = registry[-1]
# 	addDock = registry[-2]
# 	print(rmDock,addDock)

# startTimes = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip.starttime.values ] # get all starttimes in timestemp
# utils.plotHistogram(startTimes,'Tempos de ínicio')


# stopTime = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip.stoptime.values ] # get all stoptimes in timestemp
# utils.plotHistogram(stopTime,'Tempos de fim')

# stationDocks = [ int(value) for value in  station.current_dockcount.values ] # get dock counts stations
# utils.plotHistogram(stationDocks,'Vagas de estações')
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

numSample = 25000
trip = pd.read_csv('data/trip.csv', sep =',', names=tripFields)[:numSample] # read data trips

# startTimes = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip[:25000].starttime.values ]
# utils.plotHistogram(startTimes,'Tempos de chegada')
# tripDurations = [ float(milisec.replace('.','')) for milisec in  trip[:25000].tripduration.values ] # get 25000 tripduration in milisec
# utils.plotHistogram(tripDurations,'Tempo de viagens')

station = pd.read_csv('data/station.csv', sep =',', names=stationFields) # read data stations

dictStations = { name:{'bikes':0, 'docks':count,'docksAvailable':count} for name,count in station.values }

bikeIds = set(trip.bikeid)

for registry in trip.values:
	rmBike = registry[2] # bikeid 
	fromStationId = registry[5] # station_id
	if rmBike in bikeIds:
		bikeIds.remove(rmBike)
		dictStations[fromStationId]['bikes'] += 1
		dictStations[fromStationId]['docksAvailable'] -= 1

stationInitFile = open('data/station-init.csv','w')
stationInitFile.write('name,bikes,docks,docksAvailable\n')

for name in dictStations:
	result = ','.join(map(str,dictStations[name].values()))
	stationInitFile.write(name+','+result+'\n')

from Entidades import Estacao, Usuario, simpy

env = simpy.Environment()

dictStationsEnv = dict()
for key in dictStations:
	name = key
	bikeInit = dictStations[key]['bikes']
	docks = dictStations[key]['docks']
	docksAvailable = dictStations[key]['docksAvailable']

	dictStationsEnv[name] = Estacao(
		env,
		name,
		simpy.Container(env, init=bikeInit, capacity=docks),
		docksAvailable
	)
	# print(name,bikeInit,docks,docksAvailable)

usuarios = list()

contUser = 0
for registry in trip[:100].values:
	contUser += 1
	tempoChegada = utils.strToDatetime(registry[0]).timestamp()
	tempoViagem = utils.strSecToMilisec(registry[3])
	nome = 'US-'+str(contUser)
	estacaoOrig = registry[4]
	estacaoDest = dictStationsEnv[registry[5]]
	usuarios.append(Usuario(env,nome,tempoChegada,tempoViagem,estacaoOrig,estacaoDest))

for usuario in usuarios:
	stationName = usuario.estacaoOrigem
	env.process(dictStationsEnv[stationName].emprestaBicicleta(usuario))

env.run()
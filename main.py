import pandas as pd
import simpy
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
	'install_dockcount'
	]

trip = pd.read_csv('data/trip.csv', sep =',', names=tripFields)# read data trips

# startTimes = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip[:25000].starttime.values ]
# utils.plotHistogram(startTimes,'Tempos de chegada')
# tripDurations = [ float(milisec.replace('.','')) for milisec in  trip[:25000].tripduration.values ] # get 25000 tripduration in milisec
# utils.plotHistogram(tripDurations,'Tempo de viagens')

# simulation
env = simpy.Environment()

e1 = Entidades.Estacao(
    env,
    'CBD-06',
    simpy.Resource(env, capacity=5)
)

cont = 0
usuarios = list()
for registry in trip[:7].values:
	cont += 1
	nomeUsuario = 'Usuario'+str(cont)
	tempoChegada = utils.strToDatetime(registry[0]).timestamp()
	tempoViagem = utils.strSecToMilisec(registry[3])

	print(nomeUsuario,tempoChegada,tempoViagem,sep=',')
	usuarios.append(Entidades.Usuario(env,nomeUsuario,tempoChegada,tempoViagem))

for usuario in usuarios:
    env.process(e1.emprestaBicicleta(usuario))

env.run()

# station = pd.read_csv('data/station.csv', sep =',', names=stationFields) # read data stations

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
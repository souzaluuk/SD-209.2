import pandas as pd
import utils
from random import choice,seed
seed(2)


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

numSample = 1000
trip = pd.read_csv('data/trip.csv', sep =',', names=tripFields)[:numSample] # read data trips
numStations = 10
station = pd.read_csv('data/station.csv', sep =',', names=stationFields)[:numStations] # read data stations

# Descomente de 26 a 30 para plotar os Histogramas
# startTimes = [ utils.strToDatetime(date_str).timestamp() for date_str in  trip.starttime.values ]
# utils.plotHistogram(startTimes,'Tempos de chegada',op=1) # op = 1 para converter para data
# tripDurations = [ float(milisec.replace('.','')) for milisec in  trip.tripduration.values ] # get 25000 tripduration in milisec
# utils.plotHistogram(tripDurations,'Tempo de viagens',op=2) # op = 2 converte para minutos

# Demanda por vaga 33:56
# originStations = list(trip.from_station_id.values)
# demandByStation = [ (stationName,originStations.count(stationName)) for stationName in set(originStations) ]
# demandByStation.sort(key=lambda tpl: tpl[1])
# meio = len(demandByStation)
# demandByStation = demandByStation[meio//4:]
# x = [ x for x,_ in demandByStation]
# y = [ y for _,y in demandByStation]

# fig, ax1 = utils.plt.subplots()

# ax1.bar(x,y,)
# ax1.set_ylabel('Retiradas', color='b')
# utils.plt.xticks(rotation=60)

# dictStations = { name: count for name,count in station.values }

# ax2 = ax1.twinx()
# ax2.set_ylabel('Vagas', color='r')
# ax2.plot(x,[dictStations[name] for name in x], color='r')
# # utils.plt.bar(range(len(x)),[dictStations[name]*200 for name in x],color='r')
# utils.plt.title('Demanda de retirada por quantidade de vagas')
# utils.plt.show()

# exit()

# dictStations = { name:{'bikes':0, 'docks':count,'docksAvailable':count} for name,count in station.values }
dictStations = { name:{'bikes':count//4+count//2, 'docks':count,'docksAvailable':count-(count//4+count//2)} for name,count in station.values }
print('Cenário inicia com:')
print('Numero de usuários:',numSample)
for x in dictStations:
	print(x,':',dictStations[x])
print()

# bikeIds = set(trip.bikeid)

# for registry in trip.values:
# 	rmBike = registry[2] # bikeid 
# 	fromStationId = registry[5] # station_id
# 	if rmBike in bikeIds and fromStationId in dictStations:
# 		bikeIds.remove(rmBike)
# 		if dictStations[fromStationId]['bikes'] < dictStations[fromStationId]['docks']: # todas as vagas ficaram preenchidas
# 			dictStations[fromStationId]['bikes'] += 1
# 			dictStations[fromStationId]['docksAvailable'] -= 1
# 		# dictStations[fromStationId]['bikes'] += 1
# 		# dictStations[fromStationId]['docksAvailable'] -= 1
# print(dictStations)
# exit()
stationInitFile = open('data/station-init.csv','w')
stationInitFile.write('name,bikes,docks,docksAvailable\n')

for name in dictStations:
	result = ','.join(map(str,dictStations[name].values()))
	stationInitFile.write(name+','+result+'\n')

stationInitFile.close()

from Entidades import Estacao, Usuario, simpy

env = simpy.Environment()

# print(dictStations)
# exit()
dictStationsEnv = dict()
for key in dictStations:
	name = key
	bikeInit = dictStations[key]['bikes']
	docks = dictStations[key]['docks']
	docksAvailable = dictStations[key]['docksAvailable']

	dictStationsEnv[name] = Estacao(
		env,
		name,
		simpy.Container(env, init=bikeInit, capacity=docks)
	)
	# print(name,bikeInit,docks,docksAvailable)

usuarios = list()

contUser = 0
for registry in trip[:100].values:
	contUser += 1
	tempoChegada = utils.strToDatetime(registry[0]).timestamp()
	tempoViagem = utils.strSecToMilisec(registry[3])
	nome = 'US-'+str(contUser)
	estacaoOrig = choice(list(dictStations.keys()))
	estacaoDest = dictStationsEnv[choice(list(dictStations.keys()))]
	usuarios.append(Usuario(env,nome,tempoChegada,tempoViagem,estacaoOrig,estacaoDest))

for usuario in usuarios:
	stationName = usuario.estacaoOrigem
	env.process(dictStationsEnv[stationName].emprestaBicicleta(usuario))

env.run()
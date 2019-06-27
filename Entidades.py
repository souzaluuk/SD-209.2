import simpy
import utils

class Usuario:
    def __init__(self, env, nome, tempoChegada, tempoViagem, estacaoOrig, estacaoDest):
        self.env = env
        self.nome = nome
        self.tempoChegada = tempoChegada
        self.tempoViagem = tempoViagem
        self.estacaoOrigem = estacaoOrig
        self.estacaoDest = estacaoDest

class Estacao:
    def __init__(self, env, nome, bicicletas):
        self.env = env
        self.nome = nome
        self.bicicletas = bicicletas # container
        self.temBicicleta = self.env.event()
        self.temVaga = self.env.event()
    
    def emprestaBicicleta(self,usuario:Usuario):
        yield self.env.timeout(usuario.tempoChegada)
        print(usuario.nome,'chegou para aluguel em',utils.timestampToDate(self.env.now),'na estacao',self.nome)

        yield self.bicicletas.get(1)

        print(usuario.nome,'iniciou viagem no tempo',utils.timestampToDate(self.env.now),'saindo de',self.nome)
        print('Bicicletas na',self.nome,':',self.bicicletas.level)
        print('Vagas na',self.nome,':',self.bicicletas.capacity-self.bicicletas.level)
        print('Terminará em',utils.timestampToDate(self.env.now+usuario.tempoViagem//1000),'\n')

        self.temBicicleta = self.env.event()
        tempoDevolucao = usuario.tempoViagem//1000
        self.env.process(usuario.estacaoDest.devolveBicicleta(usuario,tempoDevolucao))
    
    def devolveBicicleta(self,usuario:Usuario,tempoDevolucao):
        yield self.env.timeout(tempoDevolucao)
        print(usuario.nome,'chegou para devolução em',utils.timestampToDate(self.env.now),'na estacao',self.nome)

        yield self.bicicletas.put(1)
        
        print(usuario.nome,'devolveu no tempo',utils.timestampToDate(self.env.now),'em',self.nome)
        print('Bicicletas na',self.nome,':',self.bicicletas.level)
        print('Vagas na',self.nome,':',self.bicicletas.capacity-self.bicicletas.level,'\n')
        
        self.temVaga = self.env.event()
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
    def __init__(self, env, nome, bicicletas, vagas):
        self.env = env
        self.nome = nome
        self.bicicletas = bicicletas # container
        self.vagas = vagas # resource
        self.temBicicleta = self.env.event()
        self.temVaga = self.env.event()
    
    def emprestaBicicleta(self,usuario:Usuario):
        yield self.env.timeout(usuario.tempoChegada)
        print(usuario.nome,'chegou para emprestimo em',utils.timestampToDate(self.env.now),'na estacao',self.nome)

        if 0 < self.bicicletas.level and not self.temBicicleta.triggered:
            self.temBicicleta.succeed()
    
        qtBicicletas = self.bicicletas.level-1

        yield self.temBicicleta and self.bicicletas.get(1)

        self.vagas += 1
        print(usuario.nome,'iniciou viagem saindo de', usuario.estacaoOrigem,'em',utils.timestampToDate(self.env.now))
        print('Bicicletas em',self.nome,':',qtBicicletas)
        print('Vagas em',self.nome,':',self.vagas)
        print('Terminará em',utils.timestampToDate(self.env.now+usuario.tempoViagem//1000))

        self.temBicicleta = self.env.event()
        tempoDevolucao = usuario.tempoViagem//1000
        self.env.process(usuario.estacaoDest.devolveBicicleta(usuario,tempoDevolucao))
    
    def devolveBicicleta(self,usuario:Usuario,tempoDevolucao):
        yield self.env.timeout(tempoDevolucao)
        print(usuario.nome,'chegou para devolucao em',utils.timestampToDate(self.env.now),'na estacao',self.nome)
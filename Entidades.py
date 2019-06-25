class Usuario:
    def __init__(self, env, nome, tempoChegada, tempoViagem):
        self.env = env
        self.nome = nome
        self.tempoChegada = tempoChegada
        self.tempoViagem = tempoViagem

class Estacao:
    def __init__(self, env, nome, vagas):
        self.env = env
        self.nome = nome
        self.vagas = vagas
    
    def emprestaBicicleta(self, usuario:Usuario):
        yield self.env.timeout(usuario.tempoChegada)
        print(usuario.nome, 'chegou na estação em ', self.env.now)

        with self.vagas.request() as vaga:
            yield vaga
            print(usuario.nome, 'alugou a bicicleta em ', self.env.now)
            yield self.env.timeout(usuario.tempoChegada)
            print(usuario.nome, 'devolveu a bicicleta em ', self.env.now)
            return self.vagas.release(self.env.now)
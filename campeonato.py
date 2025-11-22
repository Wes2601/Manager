from datetime import date

class Campeonato:
    def __init__(self, times, ano_inicial):
        self.times = times
        self.ano_inicial = ano_inicial
        self.data_atual = date(ano_inicial, 1, 20)
        self.time_doUsuario = times [0]
        self.todos_os_jogadores = []
        for time in self.times:
            self.todos_os_jogadores.extend(time.elenco)


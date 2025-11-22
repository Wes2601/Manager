from datetime import date, timedelta
from tabela import TabelaDeClassificacao
from calendario import Calendario
import random  # <-- Importante para o placar funcionar


class Campeonato:

    def __init__(self, times, ano_inicial):
        self.times = times
        self.ano_atual = ano_inicial
        self.data_atual = date(ano_inicial, 1, 20)
        self.time_do_usuario = times[0]

        self.todos_os_jogadores = []
        for time in self.times:
            self.todos_os_jogadores.extend(time.elenco)

        self.tabela = TabelaDeClassificacao(times)
        self.calendario = Calendario(times, self.data_atual)

    def avancar_um_dia(self):
        """Avança a data em 1 dia e processa recuperações."""
        for jogador in self.todos_os_jogadores:
            if jogador.esta_lesionado:
                # CORREÇÃO AQUI: É underline (_), não traço (-)
                msg = jogador.processar_recuperacao_diaria(10)
                if msg:
                    print(f"[NOTÍCIA] {msg}")

        self.data_atual += timedelta(days=1)

    def get_jogos_de_hoje(self):
        """Retorna a lista de partidas agendadas para a data atual."""
        return self.calendario.jogos_agendados.get(self.data_atual, [])

    def simular_jogos_de_hoje(self):
        """Simula as partidas do dia e atualiza a tabela."""
        jogos = self.get_jogos_de_hoje()

        for partida in jogos:
            placar_casa = random.randint(0, 3)
            placar_visitante = random.randint(0, 3)

            partida.placar_casa = placar_casa
            partida.placar_visitante = placar_visitante

            self.tabela.atualizar(partida.time_casa, placar_casa, placar_visitante)
            self.tabela.atualizar(partida.time_visitante, placar_visitante, placar_casa)

            print(f"JOGO: {partida.time_casa.nome} {placar_casa} x {placar_visitante} {partida.time_visitante.nome}")

        return jogos
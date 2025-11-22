from datetime import timedelta

from partida import Partida


class Calendario:
    def __init__(self, times, data_inicio):
        self.jogos_agendados = {}
        self.gerar_calendario(times, data_inicio)

    def gerar_calendario(self, times, data_atual):
        time_fixo = times[0]
        outros_times = times[1:]

        num_rodadas = len(times) - 1

        for rodada in range(num_rodadas):
            jogos_da_rodada = []

            adversario_fixo = outros_times[-1]

            if rodada % 2 == 0:
                jogos_da_rodada.append(Partida(time_fixo, adversario_fixo))
            else:
                jogos_da_rodada.append(Partida(adversario_fixo, time_fixo))

            for i in range(len(outros_times) // 2):
                time_casa = outros_times[i]
                time_visitante = outros_times[-2 - i]

                if rodada % 2 == 0:
                    jogos_da_rodada.append(Partida(time_casa, time_visitante))
                else:
                    jogos_da_rodada.append(Partida(time_visitante, time_casa))

            while data_atual.weekday() != 2 and data_atual.weekday() != 6:
                data_atual += timedelta(days=1)

            self.jogos_agendados[data_atual] = jogos_da_rodada

            data_atual += timedelta(days=1)
            ultimo = outros_times.pop()
            outros_times.insert(0, ultimo)
from datetime import date, timedelta
from partida import Partida
import random


class Calendario:
    def __init__(self, times, ano):
        self.jogos_agendados = {}
        data_inicio = date(ano, 1, 1)
        self.gerar_calendario(times, data_inicio)

    def gerar_calendario(self, times, data_atual):
        while data_atual.weekday() != 2 and data_atual.weekday() != 6:
            data_atual += timedelta(days=1)

        num_times = len(times)
        if num_times % 2 != 0:
            times.append(None)
            num_times += 1

        total_rodadas = num_times - 1
        metade = num_times // 2

        lista_times = times[:]

        for rodada in range(total_rodadas):
            jogos_da_rodada = []

            for i in range(metade):
                time_a = lista_times[i]
                time_b = lista_times[num_times - 1 - i]

                if time_a and time_b:
                    if rodada % 2 == 0:
                        partida = Partida(time_a, time_b)
                    else:
                        partida = Partida(time_b, time_a)
                    jogos_da_rodada.append(partida)

            self.jogos_agendados[data_atual] = jogos_da_rodada

            dias_para_proximo = 4 if data_atual.weekday() == 2 else 3
            data_atual += timedelta(days=dias_para_proximo)

            lista_times.insert(1, lista_times.pop())

        lista_times = times[:]
        data_atual += timedelta(days=7)

        for rodada in range(total_rodadas):
            jogos_da_rodada = []

            for i in range(metade):
                time_a = lista_times[i]
                time_b = lista_times[num_times - 1 - i]

                if time_a and time_b:
                    if rodada % 2 == 0:
                        partida = Partida(time_b, time_a)
                    else:
                        partida = Partida(time_a, time_b)
                    jogos_da_rodada.append(partida)

            self.jogos_agendados[data_atual] = jogos_da_rodada

            dias_para_proximo = 4 if data_atual.weekday() == 2 else 3
            data_atual += timedelta(days=dias_para_proximo)

            lista_times.insert(1, lista_times.pop())
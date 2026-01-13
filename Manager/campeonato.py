from datetime import date, timedelta
import random
from tabela import Tabela


class Jogo:
    def __init__(self, time_casa, time_visitante, rodada, data_jogo):
        self.time_casa = time_casa
        self.time_visitante = time_visitante
        self.rodada = rodada
        self.data_jogo = data_jogo
        self.placar_casa = 0
        self.placar_visitante = 0
        self.foi_jogado = False


class Campeonato:
    def __init__(self, times, ano):
        self.times = times
        self.ano = ano
        self.tabela = Tabela(times)
        self.jogos = []

        self.time_do_usuario = next((t for t in times if t.nome == "Flamengo"), times[0])

        self.data_atual = date(ano, 1, 1)

        self.gerar_calendario()

    def gerar_calendario(self):
        random.shuffle(self.times)
        num_times = len(self.times)
        total_rodadas = (num_times - 1) * 2

        jogos_por_rodada = num_times // 2

        mapa_times = self.times[:]

        data_rodada = self.data_atual

        for rodada in range(1, total_rodadas + 1):
            while data_rodada.weekday() != 2 and data_rodada.weekday() != 6:
                data_rodada += timedelta(days=1)

            if rodada <= num_times - 1:
                mandantes = mapa_times[:jogos_por_rodada]
                visitantes = mapa_times[jogos_por_rodada:]
                visitantes.reverse()
            else:
                mandantes = mapa_times[jogos_por_rodada:]
                mandantes.reverse()
                visitantes = mapa_times[:jogos_por_rodada]

            for i in range(jogos_por_rodada):
                if rodada <= num_times - 1:
                    jogo = Jogo(mandantes[i], visitantes[i], rodada, data_rodada)
                else:
                    jogo = Jogo(visitantes[i], mandantes[i], rodada, data_rodada)

                self.jogos.append(jogo)

            mapa_times = [mapa_times[0]] + [mapa_times[-1]] + mapa_times[1:-1]

            data_rodada += timedelta(days=1)

    def get_jogos_de_hoje(self):
        return [j for j in self.jogos if j.data_jogo == self.data_atual]

    def avancar_um_dia(self):
        self.simular_jogos_de_hoje()

        if self.data_atual.weekday() == 0:
            print(f"--- DIA DE PAGAMENTO: {self.data_atual.strftime('%d/%m/%Y')} ---")
            for time in self.times:
                custo_semanal = time.folha_salarial
                time.saldo_em_caixa -= custo_semanal

                if time == self.time_do_usuario:
                    print(
                        f"💰 Salários pagos! Valor: R$ {custo_semanal:,.2f}. Saldo restante: R$ {time.saldo_em_caixa:,.2f}")

        self.data_atual += timedelta(days=1)

    def simular_jogos_de_hoje(self):
        jogos_hoje = self.get_jogos_de_hoje()

        for jogo in jogos_hoje:
            forca_casa = jogo.time_casa.forca_ataque + jogo.time_casa.forca_defesa
            forca_visitante = jogo.time_visitante.forca_ataque + jogo.time_visitante.forca_defesa

            fator_casa = 1.10
            chance_casa = (forca_casa * fator_casa) / ((forca_casa * fator_casa) + forca_visitante)

            aleatorio = random.random()

            if aleatorio < chance_casa:
                jogo.placar_casa = random.randint(1, 3)
                jogo.placar_visitante = random.randint(0, 1)
            elif aleatorio < chance_casa + 0.25:
                gols = random.randint(0, 2)
                jogo.placar_casa = gols
                jogo.placar_visitante = gols
            else:
                jogo.placar_casa = random.randint(0, 1)
                jogo.placar_visitante = random.randint(1, 3)

            jogo.foi_jogado = True

            self.tabela.atualizar(jogo.time_casa, jogo.placar_casa, jogo.placar_visitante)
            self.tabela.atualizar(jogo.time_visitante, jogo.placar_visitante, jogo.placar_casa)

            renda, publico = jogo.time_casa.receber_bilheteria()

            if jogo.time_casa == self.time_do_usuario:
                print(f"🏟️ JOGO EM CASA! Público: {publico} | Renda: R$ {renda:,.2f} entrou no caixa.")
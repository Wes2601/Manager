import random
from datetime import date, timedelta


class Jogo:
    def __init__(self, time_casa, time_visitante):
        self.time_casa = time_casa
        self.time_visitante = time_visitante
        self.placar_casa = 0
        self.placar_visitante = 0
        self.foi_jogado = False
        self.autores_casa = []
        self.autores_visitante = []
        self.lesionados = []
        self.cartoes = []


class ClassificacaoTime:
    def __init__(self, time):
        self.time = time
        self.pontos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_pro = 0
        self.gols_contra = 0

    def saldo_gols(self):
        return self.gols_pro - self.gols_contra


class Campeonato:
    def __init__(self, times, ano):
        self.times = times
        self.ano = ano
        self.rodadas = []
        self.tabela = {time.nome: ClassificacaoTime(time) for time in times}
        self.data_inicial = date(ano, 1, 15)
        self.data_atual = self.data_inicial
        self.time_do_usuario = random.choice(times)

        self.gerar_calendario()

    def gerar_calendario(self):
        self.rodadas = []
        times_copia = self.times[:]
        random.shuffle(times_copia)

        num_times = len(times_copia)
        rodadas_turno = []

        for _ in range(num_times - 1):
            jogos_desta_rodada = []

            for i in range(num_times // 2):
                time1 = times_copia[i]
                time2 = times_copia[num_times - 1 - i]

                if _ % 2 == 0:
                    jogo = Jogo(time1, time2)
                else:
                    jogo = Jogo(time2, time1)

                jogos_desta_rodada.append(jogo)

            rodadas_turno.append(jogos_desta_rodada)

            times_copia.insert(1, times_copia.pop())

        rodadas_returno = []
        for rodada_turno in rodadas_turno:
            jogos_volta = []
            for jogo_ida in rodada_turno:
                jogos_volta.append(Jogo(jogo_ida.time_visitante, jogo_ida.time_casa))
            rodadas_returno.append(jogos_volta)

        self.rodadas = rodadas_turno + rodadas_returno

    def get_jogos_de_hoje(self):
        dias_passados = (self.data_atual - self.data_inicial).days
        indice_rodada = dias_passados // 3

        if 0 <= indice_rodada < len(self.rodadas):
            return self.rodadas[indice_rodada], indice_rodada + 1
        return [], 0

    def avancar_um_dia(self):
        self.tratar_lesoes_globais()

        jogos, numero_rodada = self.get_jogos_de_hoje()

        if jogos and not jogos[0].foi_jogado:
            print(f"\n=== RESULTADOS DA RODADA {numero_rodada}/38 ({self.data_atual.strftime('%d/%m')}) ===")

            for jogo in jogos:
                self.simular_partida(jogo)

            self.mostrar_resumo_usuario(numero_rodada)

        else:
            print(f"Dia {self.data_atual.strftime('%d/%m')}: Treino e recuperação.")

        if self.data_atual.weekday() == 0:
            self.processar_financas()

        self.data_atual += timedelta(days=1)

    def tratar_lesoes_globais(self):
        for time in self.times:
            for jogador in time.elenco:
                if jogador.recuperacao > 0:
                    jogador.recuperacao -= 1

    def simular_partida(self, jogo):
        suspensos_casa = [j for j in jogo.time_casa.elenco if j.suspenso]
        suspensos_visitante = [j for j in jogo.time_visitante.elenco if j.suspenso]

        chance_casa = jogo.time_casa.forca_ataque
        chance_visitante = jogo.time_visitante.forca_ataque

        jogo.placar_casa = int(random.triangular(0, 4, chance_casa / 20))
        jogo.placar_visitante = int(random.triangular(0, 4, chance_visitante / 20))
        jogo.foi_jogado = True

        jogo.autores_casa = self.gerar_artilheiros(jogo.time_casa, jogo.placar_casa)
        jogo.autores_visitante = self.gerar_artilheiros(jogo.time_visitante, jogo.placar_visitante)

        self.aplicar_lesoes_jogo(jogo)
        self.aplicar_cartoes_jogo(jogo)

        self.atualizar_tabela(jogo)

        for j in suspensos_casa: j.suspenso = False
        for j in suspensos_visitante: j.suspenso = False

        prefixo = "   "
        if jogo.time_casa == self.time_do_usuario or jogo.time_visitante == self.time_do_usuario:
            prefixo = "👉 "

        print(f"{prefixo}{jogo.time_casa.nome} {jogo.placar_casa} x {jogo.placar_visitante} {jogo.time_visitante.nome}")

        infos_extras = []
        if jogo.lesionados: infos_extras.append(f"🚑 Lesão: {', '.join(jogo.lesionados)}")
        if jogo.cartoes: infos_extras.append(f"🟥/🟨: {', '.join(jogo.cartoes)}")

        if (jogo.time_casa == self.time_do_usuario or jogo.time_visitante == self.time_do_usuario) and infos_extras:
            print(f"      {' | '.join(infos_extras)}")

        if jogo.time_casa == self.time_do_usuario:
            renda, publico = jogo.time_casa.receber_bilheteria()
            print(f"      Bilheteria: R$ {renda:,.2f}")

    def aplicar_lesoes_jogo(self, jogo):
        todos = jogo.time_casa.elenco + jogo.time_visitante.elenco
        for jogador in todos:
            if not jogador.esta_lesionado and not jogador.suspenso:
                if random.random() < 0.01:
                    dias = random.randint(3, 14)
                    jogador.recuperacao = dias
                    jogo.lesionados.append(f"{jogador.nome} ({dias}d)")

    def aplicar_cartoes_jogo(self, jogo):
        todos = jogo.time_casa.elenco + jogo.time_visitante.elenco
        for jogador in todos:
            if not jogador.esta_lesionado and not jogador.suspenso:
                if random.random() < 0.05:
                    jogador.cartoes_amarelos += 1
                    if jogador.cartoes_amarelos >= 3:
                        jogador.suspenso = True
                        jogador.cartoes_amarelos = 0
                        jogo.cartoes.append(f"{jogador.nome} (3º Amarelo)")

                elif random.random() < 0.005:
                    jogador.suspenso = True
                    jogo.cartoes.append(f"{jogador.nome} (Vermelho)")

    def gerar_artilheiros(self, time, gols):
        lista_nomes = []
        if gols > 0:
            atacantes = [j for j in time.elenco if
                         ("Atacante" in j.funcao or "Meio" in j.funcao) and not j.esta_lesionado and not j.suspenso]
            if not atacantes: atacantes = time.elenco

            for _ in range(gols):
                autor = random.choice(atacantes)
                lista_nomes.append(autor.nome)
        return lista_nomes

    def atualizar_tabela(self, jogo):
        c_casa = self.tabela[jogo.time_casa.nome]
        c_casa.gols_pro += jogo.placar_casa
        c_casa.gols_contra += jogo.placar_visitante

        c_vis = self.tabela[jogo.time_visitante.nome]
        c_vis.gols_pro += jogo.placar_visitante
        c_vis.gols_contra += jogo.placar_casa

        if jogo.placar_casa > jogo.placar_visitante:
            c_casa.pontos += 3
            c_casa.vitorias += 1
            c_vis.derrotas += 1
        elif jogo.placar_visitante > jogo.placar_casa:
            c_vis.pontos += 3
            c_vis.vitorias += 1
            c_casa.derrotas += 1
        else:
            c_casa.pontos += 1
            c_casa.empates += 1
            c_vis.pontos += 1
            c_vis.empates += 1

    def mostrar_resumo_usuario(self, rodada):
        classificacao = sorted(self.tabela.values(), key=lambda p: (p.pontos, p.vitorias, p.saldo_gols()), reverse=True)

        posicao = 0
        meu_pontos = 0
        for i, classif in enumerate(classificacao):
            if classif.time == self.time_do_usuario:
                posicao = i + 1
                meu_pontos = classif.pontos
                break

        print(f"Resumo Rodada {rodada}: Seu time está em {posicao}º ({meu_pontos} pts)")

    def processar_financas(self):
        print("\n--- PAGAMENTO DE SALÁRIOS ---")
        for time in self.times:
            folha = time.folha_salarial
            time.saldo_em_caixa -= folha
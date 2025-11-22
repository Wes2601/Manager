from datetime import date
import random

from clube import Time
from campeonato import Campeonato
from jogador import Jogador
from contrato import Contrato

def gerar_elenco_inicial(time_id):
    elenco = []
    posicoes = ["Goleiro", "Zagueiro", "Lateral", "Volante", "Meia", "Atacante"]
    nomes_base = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Ferreira", "Costa"]

    for i in range(15):
        nome = f"Jogador {i} {random.choice(nomes_base)}"
        id_jogador = (time_id * 100) + i
        posicao = random.choice(posicoes)
        ano_nasc = random.randint(1990, 2005)

        contrato = Contrato(
            salario_semanal=random.randint(1000, 50000),
            data_expiracao=date(2027, 12, 31)
        )

        novo_jogador = Jogador(
            nome=nome,
            id=id_jogador,
            nacionalidade="BRA",
            data_nascimento=date(ano_nasc, 1, 1),
            funcao=posicao,
            potencial=random.randint(100, 180),
            contrato=contrato
        )
        elenco.append(novo_jogador)

    return elenco

def criar_times_da_liga():
    nomes_times = [
        "Flamengo", "Palmeiras", "São Paulo", "Corinthians",
        "Vasco", "Fluminense", "Botafogo", "Santos",
        "Grêmio", "Internacional", "Atlético-MG", "Cruzeiro",
        "Bahia", "Vitória", "Fortaleza", "Ceará",
        "Athletico-PR", "Coritiba", "Goiás", "Sport"
    ]

    lista_times = []
    print("--- Inicializando a Liga e Contratando Jogadores ---")

    for i, nome in enumerate(nomes_times):
        novo_time = Time(id=i, nome=nome, saldo_inicial=50000000)

        jogadores = gerar_elenco_inicial(i)
        for jog in jogadores:
            novo_time.adicionar_jogador(jog)

        lista_times.append(novo_time)
        print(f"Time criado: {nome} ({len(jogadores)} jogadores)")

    return lista_times

if __name__ == "__main__":
    times = criar_times_da_liga()

    campeonato = Campeonato(times, 2025)

    print("\n" + "="*40)
    print(f"BEM-VINDO AO PYTHON FOOTBALL MANAGER 2025")
    print(f"Você é o técnico do: {campeonato.time_do_usuario.nome}")
    print("="*40 + "\n")

    while True:
        print(f"\n--- DATA: {campeonato.data_atual} ---")

        jogos_hoje = campeonato.simular_jogos_de_hoje()

        if jogos_hoje:
            print(f"HOJE TEVE {len(jogos_hoje)} PARTIDAS!")
            for p in jogos_hoje:
                if p.time_casa == campeonato.time_do_usuario or p.time_visitante == campeonato.time_do_usuario:
                    print(f">>> SEU JOGO: {p.time_casa.nome} {p.placar_casa} x {p.placar_visitante} {p.time_visitante.nome}")

        acao = input("\n[Enter] Avançar Dia  |  [t] Ver Tabela  |  [s] Sair: ").lower()

        if acao == 's':
            print("Saindo...")
            break

        elif acao == 't':
            print("\n--- CLASSIFICAÇÃO ---")
            tabela_ordenada = sorted(campeonato.tabela.posicoes.values(), key=lambda p: p.pontos, reverse=True)
            for i, posicao in enumerate(tabela_ordenada[:10]):
                print(f"{i+1}º {posicao.time.nome}: {posicao.pontos} pts")
            input("[Pressione Enter para voltar]")

        else:
            campeonato.avancar_um_dia()
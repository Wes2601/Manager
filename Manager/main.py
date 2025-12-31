from clube import Time
from jogador import Jogador
from datetime import date
import random


def criar_times_da_liga():
    nomes_times = [
        "Flamengo", "Palmeiras", "Atlético-MG", "São Paulo",
        "Fluminense", "Grêmio", "Internacional", "Corinthians",
        "Santos", "Vasco", "Botafogo", "Cruzeiro",
        "Bahia", "Fortaleza", "Athletico-PR", "Cuiabá",
        "Goiás", "Coritiba", "América-MG", "Red Bull Bragantino"
    ]

    lista_de_objetos_time = []

    nomes_jogadores = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima",
                       "Gomes"]
    prenomes = ["Gabriel", "Lucas", "Matheus", "Pedro", "Guilherme", "Gustavo", "Rafael", "Felipe", "João", "Enzo"]
    posicoes = ["Goleiro", "Zagueiro", "Lateral", "Volante", "Meia", "Atacante"]

    for i, nome_time in enumerate(nomes_times):
        if nome_time in ["Flamengo", "Palmeiras"]:
            saldo = 50000000
        elif nome_time in ["Vasco", "Botafogo", "Cruzeiro"]:
            saldo = 25000000
        else:
            saldo = 10000000

        novo_time = Time(i, nome_time, saldo)

        for j in range(22):
            nome_completo = f"{random.choice(prenomes)} {random.choice(nomes_jogadores)}"

            base_potencial = 70 if saldo > 30000000 else 50
            potencial = random.randint(base_potencial, 95)

            ano_nasc = 2025 - random.randint(16, 35)

            novo_jogador = Jogador(
                nome=nome_completo,
                id=f"{i}-{j}",
                nacionalidade="Brasil",
                data_nascimento=date(ano_nasc, 1, 1),
                funcao=random.choice(posicoes),
                potencial=potencial,
                contrato=2026
            )

            novo_time.adicionar_jogador(novo_jogador)

        lista_de_objetos_time.append(novo_time)

    return lista_de_objetos_time
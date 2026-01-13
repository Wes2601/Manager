from clube import Time
from jogador import Jogador
from datetime import date
import random


def criar_times_da_liga():
    nomes_times = [
        "Flamengo", "Palmeiras", "São Paulo", "Corinthians",
        "Vasco", "Fluminense", "Botafogo", "Grêmio",
        "Inter", "Atlético-MG", "Cruzeiro", "Bahia",
        "Fortaleza", "Athletico-PR", "Santos", "Bragantino",
        "Criciúma", "Juventude", "Vitória", "Atlético-GO"
    ]

    lista_objetos_times = []

    nomes_masculinos = ["Carlos", "André", "Felipe", "Lucas", "Matheus", "Gabriel", "Pedro", "João", "Rafael", "Bruno",
                        "Thiago", "Luiz", "Gustavo", "Rodrigo", "Fábio"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Ferreira", "Costa", "Rodrigues",
                  "Almeida", "Nascimento", "Alves", "Carvalho", "Araújo", "Ribeiro"]

    for nome_time in nomes_times:
        novo_time = Time(nome_time, random.randint(1000, 9999), "Brasil")

        esquema = [("Goleiro", 2), ("Defensor", 8), ("Meio-Campista", 8), ("Atacante", 4)]

        for funcao, quantidade in esquema:
            for _ in range(quantidade):
                nome_completo = f"{random.choice(nomes_masculinos)} {random.choice(sobrenomes)}"

                base_pot = 70
                if nome_time in ["Flamengo", "Palmeiras", "Atlético-MG"]:
                    base_pot = 78

                potencial = random.randint(base_pot - 10, base_pot + 10)
                if potencial > 99: potencial = 99

                idade = random.randint(17, 36)
                ano_nasc = 2025 - idade

                novo_jogador = Jogador(
                    nome_completo,
                    random.randint(10000, 99999),
                    "Brasil",
                    date(ano_nasc, 1, 1),
                    funcao,
                    potencial,
                    2026
                )

                novo_time.adicionar_jogador(novo_jogador)

        lista_objetos_times.append(novo_time)

    return lista_objetos_times
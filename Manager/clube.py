from staff import Staff, Cargo
from tatica import Tatica
from caixa_de_entrada import CaixaDeEntrada
import random

class Time:
    def __init__(self,id, nome, saldo_inicial):

        self.id = id
        self.nome = nome
        self.saldo_inicial = saldo_inicial

        self.orcamento_transferencias = saldo_inicial // 4
        self.orcamento_salario_semanal = saldo_inicial // 100
        self.salario_atual_semanal = 0

        self.elenco = []
        self.comissao_tecnica = []

        self.tatica_ativa = Tatica("4-4-2 Padrão")
        self.caixa_de_entrada = CaixaDeEntrada()

        self.comissao_tecnica.append(Staff(
            nome="Técnico" + nome,
            cargo=Cargo.TECNICO_PRINCIPAL,
            habilidade=random.randint(5,16)
        ))

        self.comissao_tecnica.append(Staff(
            nome="Olheiro" + nome,
            cargo=Cargo.OLHEIRO_CHEFE,
            habilidade=random.randint(5,16)
        ))

        self.comissao_tecnica.append(Staff(
            nome= "Fisio" + nome,
            cargo=Cargo.FISIOTERAPEUTA_CHEFE,
            habilidade=random.randint(5,16)
        ))

    def adicionar_jogador(self,jogador):
       self.elenco.append(jogador)

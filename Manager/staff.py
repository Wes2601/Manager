from enum import Enum
class Cargo(Enum):
    TECNICO_PRINCIPAL = 1
    OLHEIRO_CHEFE = 2
    FISIOTERAPEUTA_CHEFE = 3

class Staff:
    def __init__(self,cargo, nome, habilidade):
        self.cargo = cargo
        self.nome = nome
        self.habilidade = habilidade

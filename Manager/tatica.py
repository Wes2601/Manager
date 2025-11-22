class Tatica:
    def __init__(self, nome_formacao):
        self.nome_formacao = nome_formacao
        self.escalacao = {}
        self.posicoes = ["Goleiro", "Lateral Direito", "Zagueiro Direito", "Zagueiro Esquerdo", "Lateral Esquerdo", "Volante 1", "Volante 2", "Meia Direito", "Meia Esquerdo", "Atacante 1", "Atacante 2"]
        for pos in self.posicoes:
                self.escalacao[pos] = None
from datetime import date
class Mensagem:
    def __init__(self, titulo, corpo):
        self.titulo = titulo
        self.corpo = corpo
        self.data = date.today()

class CaixaDeEntrada:
    def __init__(self):
        self.mensagens = []

    def adicionar_mensagem(self, titulo, corpo):
        nova_mensagem = Mensagem(titulo, corpo)
        self.mensagens.append(nova_mensagem)
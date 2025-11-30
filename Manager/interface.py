import customtkinter as ctk
from main import criar_times_da_liga
from campeonato import Campeonato
from view_detalhes import TelaDetalhesJogador

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Manager 2025")
        self.geometry("1000x700")

        self.campeonato = None

        self.frame_menu = ctk.CTkFrame(self)
        self.frame_menu.pack(fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.frame_menu, text="Bem vindo ao jogo!", font=("Arial", 32, "bold"))
        self.label_titulo.pack(pady=80)

        self.botao_iniciar = ctk.CTkButton(self.frame_menu, text="Iniciar Novo Jogo", font=("Arial", 16), height=50,
                                           width=200, command=self.iniciar_jogo)
        self.botao_iniciar.pack(pady=10)

    def iniciar_jogo(self):
        self.label_titulo.configure(text="Criando universo...")
        self.update()

        times = criar_times_da_liga()
        self.campeonato = Campeonato(times, 2025)

        print(f"Jogo criado! Técnico do: {self.campeonato.time_do_usuario.nome}")

        self.frame_menu.pack_forget()
        self.abrir_dashboard()

    def abrir_dashboard(self):
        self.frame_dashboard = ctk.CTkFrame(self)
        self.frame_dashboard.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_info = ctk.CTkLabel(self.frame_dashboard, text="", font=("Arial", 24, "bold"))
        self.label_info.pack(pady=10)

        self.atualizar_interface()

        self.abas = ctk.CTkTabview(self.frame_dashboard)
        self.abas.pack(fill="both", expand=True, padx=10, pady=5)

        self.aba_elenco = self.abas.add("Meu Elenco")
        self.aba_tabela = self.abas.add("Classificação")
        self.aba_jogos = self.abas.add("Calendário")

        self.montar_aba_elenco()

        self.btn_avancar = ctk.CTkButton(
            self.frame_dashboard,
            text="Avançar Dia",
            fg_color="green",
            height=50,
            font=("Arial", 16, "bold"),
            command=self.acao_avancar_dia
        )
        self.btn_avancar.pack(pady=10, padx=20, fill="x")

    def montar_aba_elenco(self):
        scroll_elenco = ctk.CTkScrollableFrame(self.aba_elenco)
        scroll_elenco.pack(fill="both", expand=True)

        meu_time = self.campeonato.time_do_usuario
        meu_time.elenco.sort(key=lambda x: x.potencial, reverse=True)

        for jogador in meu_time.elenco:
            cor_texto = "red" if jogador.esta_lesionado else ("gray10", "gray90")
            texto_jog = f"{jogador.nome} ({jogador.funcao}) - Pot: {jogador.potencial}"

            btn = ctk.CTkButton(
                scroll_elenco,
                text=texto_jog,
                font=("Arial", 14),
                fg_color="transparent",
                border_width=1,
                border_color="gray",
                text_color=cor_texto,
                anchor="w",
                height=35,
                command=lambda j=jogador: self.abrir_detalhes(j)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def abrir_detalhes(self, jogador):
        TelaDetalhesJogador(self, jogador)

    def acao_avancar_dia(self):
        self.campeonato.avancar_um_dia()
        self.atualizar_interface()

    def atualizar_interface(self):
        meu_time = self.campeonato.time_do_usuario
        texto_info = f"{meu_time.nome} | R$ {meu_time.saldo_em_caixa:,.2f} | {self.campeonato.data_atual}"
        self.label_info.configure(text=texto_info)


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
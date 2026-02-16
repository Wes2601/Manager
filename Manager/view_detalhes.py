import customtkinter as ctk


class TelaDetalhesJogador(ctk.CTkToplevel):
    def __init__(self, parent, jogador):
        super().__init__(parent)

        self.title(f"Detalhes: {jogador.nome}")
        self.geometry("400x550")
        self.attributes("-topmost", True)

        lbl_nome = ctk.CTkLabel(self, text=jogador.nome, font=("Arial", 22, "bold"))
        lbl_nome.pack(pady=(20, 0))

        lbl_funcao = ctk.CTkLabel(self,
                                  text=f"{jogador.funcao} | {jogador.nacionalidade} | {2025 - jogador.data_nascimento.year} anos",
                                  text_color="gray")
        lbl_funcao.pack(pady=0)

        frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        frame_stats.pack(pady=10)

        lbl_gols = ctk.CTkLabel(frame_stats, text=f"⚽ Golos na Temporada: {jogador.gols_temporada}",
                                font=("Arial", 16, "bold"), text_color="#00FFFF")
        lbl_gols.pack()

        frame_barras = ctk.CTkFrame(self)
        frame_barras.pack(pady=10, padx=20, fill="x")

        self.criar_barra(frame_barras, "Potencial", jogador.potencial, 100, "cyan")
        self.criar_barra(frame_barras, "Condição Física", jogador.condicao_fisica, 100,
                         "green" if jogador.condicao_fisica > 70 else "red")
        self.criar_barra(frame_barras, "Moral", jogador.moral, 100, "orange")

        if jogador.esta_lesionado:
            lbl_status = ctk.CTkLabel(self, text=f"🚑 LESIONADO ({jogador.recuperacao} dias)", text_color="red",
                                      font=("Arial", 14, "bold"))
            lbl_status.pack(pady=5)
        elif jogador.suspenso:
            lbl_status = ctk.CTkLabel(self, text="🟥 SUSPENSO", text_color="red", font=("Arial", 14, "bold"))
            lbl_status.pack(pady=5)

        lbl_financas = ctk.CTkLabel(self, text="FINANÇAS", font=("Arial", 14, "bold"))
        lbl_financas.pack(pady=(10, 5))

        lbl_salario = ctk.CTkLabel(self, text=f"Salário: R$ {jogador.salario:,.2f} / semana", text_color="yellow")
        lbl_salario.pack()

        lbl_valor = ctk.CTkLabel(self, text=f"Valor: R$ {jogador.valor_mercado:,.2f}", text_color="#00FF00")
        lbl_valor.pack()

        btn_fechar = ctk.CTkButton(self, text="Fechar", command=self.destroy, fg_color="gray", hover_color="gray30")
        btn_fechar.pack(pady=20, padx=40, fill="x")

    def criar_barra(self, parent, titulo, valor, maximo, cor):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=2)

        lbl = ctk.CTkLabel(f, text=f"{titulo}: {valor}", font=("Arial", 11), width=100, anchor="w")
        lbl.pack(side="left")

        progress = ctk.CTkProgressBar(f, progress_color=cor)
        progress.set(valor / maximo)
        progress.pack(side="right", fill="x", expand=True, padx=5)
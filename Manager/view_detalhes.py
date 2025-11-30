import customtkinter as ctk


class TelaDetalhesJogador(ctk.CTkToplevel):
    def __init__(self, parent, jogador):
        super().__init__(parent)

        self.title(f"Detalhes: {jogador.nome}")
        self.geometry("400x500")
        self.attributes("-topmost", True)

        texto_header = f"{jogador.nome}\n{jogador.funcao} | {jogador.nacionalidade} | {jogador.get_idade()} anos"
        self.lbl_header = ctk.CTkLabel(self, text=texto_header, font=("Arial", 20, "bold"))
        self.lbl_header.pack(pady=10)

        texto_status = f"Moral: {jogador.moral}/100"
        if jogador.esta_lesionado:
            texto_status += f" | LESIONADO ({jogador.dias_de_molho} dias)"
            cor_status = "red"
        else:
            texto_status += " | Apto para jogo"
            cor_status = "green"

        self.lbl_status = ctk.CTkLabel(self, text=texto_status, text_color=cor_status, font=("Arial", 14))
        self.lbl_status.pack(pady=5)

        self.scroll_atributos = ctk.CTkScrollableFrame(self, label_text="Atributos Técnicos e Mentais")
        self.scroll_atributos.pack(fill="both", expand=True, padx=10, pady=10)

        for atributo, valor in jogador.atributos.items():
            linha = ctk.CTkFrame(self.scroll_atributos, fg_color="transparent")
            linha.pack(fill="x", pady=2)

            lbl_nome = ctk.CTkLabel(linha, text=atributo, anchor="w")
            lbl_nome.pack(side="left", padx=5)

            cor_valor = "cyan" if valor >= 15 else "white"
            lbl_valor = ctk.CTkLabel(linha, text=str(valor), text_color=cor_valor, font=("Arial", 14, "bold"))
            lbl_valor.pack(side="right", padx=5)

        self.btn_fechar = ctk.CTkButton(self, text="Fechar", command=self.destroy, fg_color="transparent",
                                        border_width=1)
        self.btn_fechar.pack(pady=10)
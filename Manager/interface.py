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
        self.aba_mercado = self.abas.add("Mercado")

        self.montar_aba_elenco()
        self.montar_aba_tabela()
        self.montar_aba_calendario()
        self.montar_aba_mercado()

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

    def montar_aba_tabela(self):
        for widget in self.aba_tabela.winfo_children():
            widget.destroy()

        scroll_tabela = ctk.CTkScrollableFrame(self.aba_tabela)
        scroll_tabela.pack(fill="both", expand=True)

        colunas = ["Pos", "Clube", "P", "V", "E", "D", "SG"]
        for i, col in enumerate(colunas):
            ctk.CTkLabel(scroll_tabela, text=col, font=("Arial", 14, "bold")).grid(row=0, column=i, padx=10, pady=5)

        tabela_ordenada = sorted(
            self.campeonato.tabela.posicoes.values(),
            key=lambda p: (p.pontos, p.vitorias, p.saldo_gols()),
            reverse=True
        )

        for i, posicao in enumerate(tabela_ordenada):
            dados = [
                f"{i + 1}º",
                posicao.time.nome,
                posicao.pontos,
                posicao.vitorias,
                posicao.empates,
                posicao.derrotas,
                posicao.saldo_gols()
            ]

            cor_texto = "cyan" if posicao.time == self.campeonato.time_do_usuario else ("gray10", "gray90")
            fonte_texto = ("Arial", 12, "bold") if posicao.time == self.campeonato.time_do_usuario else ("Arial", 12)

            for j, valor in enumerate(dados):
                label = ctk.CTkLabel(scroll_tabela, text=str(valor), text_color=cor_texto, font=fonte_texto)
                label.grid(row=i + 1, column=j, padx=10, pady=2)

    def montar_aba_calendario(self):
        for widget in self.aba_jogos.winfo_children():
            widget.destroy()

        scroll_jogos = ctk.CTkScrollableFrame(self.aba_jogos)
        scroll_jogos.pack(fill="both", expand=True)

        todas_as_datas = sorted(self.campeonato.calendario.jogos_agendados.keys())

        for data in todas_as_datas:
            lista_jogos = self.campeonato.calendario.jogos_agendados[data]

            data_str = data.strftime("%d/%m/%Y")
            lbl_data = ctk.CTkLabel(scroll_jogos, text=f"--- {data_str} ---", font=("Arial", 14, "bold"),
                                    text_color="yellow")
            lbl_data.pack(pady=(10, 5))

            for jogo in lista_jogos:
                if jogo.foi_jogado:
                    placar = f"{jogo.placar_casa} x {jogo.placar_visitante}"
                    cor = ("gray10", "gray90")
                else:
                    placar = "x"
                    cor = "gray"

                if jogo.time_casa == self.campeonato.time_do_usuario or jogo.time_visitante == self.campeonato.time_do_usuario:
                    cor = "cyan"
                    texto_jogo = f">> {jogo.time_casa.nome}  {placar}  {jogo.time_visitante.nome} <<"
                else:
                    texto_jogo = f"{jogo.time_casa.nome}  {placar}  {jogo.time_visitante.nome}"

                lbl_jogo = ctk.CTkLabel(scroll_jogos, text=texto_jogo, font=("Arial", 12), text_color=cor)
                lbl_jogo.pack()

    def abrir_detalhes(self, jogador):
        TelaDetalhesJogador(self, jogador)

    def acao_avancar_dia(self):
        self.campeonato.avancar_um_dia()
        self.atualizar_interface()
        self.montar_aba_tabela()
        self.montar_aba_calendario()

    def atualizar_interface(self):
        meu_time = self.campeonato.time_do_usuario
        texto_info = f"{meu_time.nome} | R$ {meu_time.saldo_em_caixa:,.2f} | {self.campeonato.data_atual}"
        self.label_info.configure(text=texto_info)

    def montar_aba_mercado(self):
        for widget in self.aba_mercado.winfo_children():
            widget.destroy()

        saldo = self.campeonato.time_do_usuario.saldo_em_caixa
        lbl_saldo = ctk.CTkLabel(self.aba_mercado, text=f"SEU SALDO: R$ {saldo:,.2f}", font=("Arial", 20, "bold"),
                                 text_color="green")
        lbl_saldo.pack(pady=10)

        scroll_mercado = ctk.CTkScrollableFrame(self.aba_mercado)
        scroll_mercado.pack(fill="both", expand=True)

        todos_jogadores = []
        for time in self.campeonato.times:
            if time != self.campeonato.time_do_usuario:
                todos_jogadores.extend(time.elenco)

        todos_jogadores.sort(key=lambda j: j.valor_mercado, reverse=True)

        for jogador in todos_jogadores[:50]:
            frame_linha = ctk.CTkFrame(scroll_mercado, fg_color="transparent")
            frame_linha.pack(fill="x", pady=2, padx=5)

            txt = f"{jogador.nome} ({jogador.funcao}) - Pot: {jogador.potencial} | R$ {jogador.valor_mercado:,.2f}"
            lbl = ctk.CTkLabel(frame_linha, text=txt, font=("Arial", 12), anchor="w")
            lbl.pack(side="left", padx=10)

            cor_btn = "green" if saldo >= jogador.valor_mercado else "gray"
            estado_btn = "normal" if saldo >= jogador.valor_mercado else "disabled"

            btn = ctk.CTkButton(
                frame_linha,
                text="Comprar",
                width=80,
                fg_color=cor_btn,
                state=estado_btn,
                command=lambda j=jogador: self.realizar_compra(j)
            )
            btn.pack(side="right", padx=10)

    def realizar_compra(self, jogador):
        meu_time = self.campeonato.time_do_usuario
        preco = jogador.valor_mercado

        if meu_time.saldo_em_caixa >= preco:
            meu_time.saldo_em_caixa -= preco

            for time in self.campeonato.times:
                if jogador in time.elenco:
                    time.elenco.remove(jogador)
                    time.saldo_em_caixa += preco
                    break

            meu_time.elenco.append(jogador)

            print(f"CONTRATAÇÃO: {jogador.nome} comprado por R$ {preco:,.2f}")

            self.montar_aba_mercado()
            self.montar_aba_elenco()
            self.atualizar_interface()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()


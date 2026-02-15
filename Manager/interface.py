import customtkinter as ctk
from campeonato import Campeonato
from main import criar_times_da_liga
from view_detalhes import TelaDetalhesJogador
from sistema_dados import salvar_jogo, carregar_jogo, existe_save

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Football Manager 2026")
        self.geometry("1000x700")

        self.campeonato = None

        self.tela_inicial()

    def tela_inicial(self):
        self.frame_inicial = ctk.CTkFrame(self)
        self.frame_inicial.pack(fill="both", expand=True)

        lbl_titulo = ctk.CTkLabel(self.frame_inicial, text="Python Football Manager", font=("Arial", 32, "bold"))
        lbl_titulo.pack(pady=50)

        btn_novo_jogo = ctk.CTkButton(self.frame_inicial, text="Iniciar Novo Jogo", command=self.iniciar_novo_jogo,
                                      width=200, height=50)
        btn_novo_jogo.pack(pady=20)

        if existe_save():
            btn_carregar = ctk.CTkButton(self.frame_inicial, text="Continuar Jogo Salvo", fg_color="green",
                                         command=self.carregar_jogo_existente, width=200, height=50)
            btn_carregar.pack(pady=10)

    def iniciar_novo_jogo(self):
        times = criar_times_da_liga()
        self.campeonato = Campeonato(times, 2025)

        print(f"Jogo criado! Técnico do: {self.campeonato.time_do_usuario.nome}")

        self.frame_inicial.destroy()
        self.abrir_dashboard()

    def carregar_jogo_existente(self):
        self.campeonato = carregar_jogo()
        if self.campeonato:
            print(f"Save carregado! Técnico do: {self.campeonato.time_do_usuario.nome}")
            self.frame_inicial.destroy()
            self.abrir_dashboard()
        else:
            print("Erro ao carregar save.")

    def abrir_dashboard(self):
        self.frame_dashboard = ctk.CTkFrame(self)
        self.frame_dashboard.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_info = ctk.CTkLabel(self.frame_dashboard, text="", font=("Arial", 24, "bold"))
        self.label_info.pack(pady=10)

        self.abas = ctk.CTkTabview(self.frame_dashboard)
        self.abas.pack(fill="both", expand=True, padx=10, pady=5)

        self.aba_elenco = self.abas.add("Meu Elenco")
        self.aba_tabela = self.abas.add("Classificação")
        self.aba_jogos = self.abas.add("Calendário")
        self.aba_mercado = self.abas.add("Mercado")

        self.atualizar_interface()

        self.btn_avancar = ctk.CTkButton(
            self.frame_dashboard,
            text="Avançar Dia",
            fg_color="green",
            height=50,
            font=("Arial", 16, "bold"),
            command=self.acao_avancar_dia
        )
        self.btn_avancar.pack(pady=10, padx=20, fill="x")

        btn_salvar = ctk.CTkButton(
            self.frame_dashboard,
            text="Salvar e Sair",
            fg_color="red",
            command=self.acao_salvar_sair
        )
        btn_salvar.pack(pady=10, padx=20, fill="x")

    def acao_salvar_sair(self):
        salvar_jogo(self.campeonato)
        self.destroy()

    def acao_avancar_dia(self):
        self.campeonato.avancar_um_dia()
        self.atualizar_interface()

    def atualizar_interface(self):
        self.montar_aba_elenco()
        self.montar_aba_tabela()
        self.montar_aba_calendario()
        self.montar_aba_mercado()

        meu_time = self.campeonato.time_do_usuario
        texto_info = f"{meu_time.nome} | R$ {meu_time.saldo_em_caixa:,.2f} | {self.campeonato.data_atual.strftime('%d/%m/%Y')}"
        self.label_info.configure(text=texto_info)

    def montar_aba_elenco(self):
        for widget in self.aba_elenco.winfo_children():
            widget.destroy()

        meu_time = self.campeonato.time_do_usuario

        lbl_titulo = ctk.CTkLabel(self.aba_elenco, text=f"Elenco do {meu_time.nome}", font=("Arial", 20, "bold"))
        lbl_titulo.pack(pady=5)

        texto_financas = f"Caixa: R$ {meu_time.saldo_em_caixa:,.2f}  |  Folha Semanal: R$ {meu_time.folha_salarial:,.2f}"
        lbl_financas = ctk.CTkLabel(self.aba_elenco, text=texto_financas, font=("Arial", 14), text_color="yellow")
        lbl_financas.pack(pady=5)

        scroll_elenco = ctk.CTkScrollableFrame(self.aba_elenco)
        scroll_elenco.pack(fill="both", expand=True)

        elenco_ordenado = sorted(meu_time.elenco, key=lambda x: x.potencial, reverse=True)

        for jogador in elenco_ordenado:
            txt_condicao = f"{jogador.condicao_fisica}%"
            texto = f"{jogador.funcao} | {jogador.nome} | Pot: {jogador.potencial} | Cond: {txt_condicao}"

            cor_texto = "gray90"
            extras = []

            if jogador.esta_lesionado:
                cor_texto = "#FF5555"
                extras.append(f"🚑 {jogador.recuperacao}d")

            if jogador.suspenso:
                cor_texto = "#FF0000"
                extras.append("🟥 SUSPENSO")
            elif jogador.cartoes_amarelos > 0:
                amarelos = "🟨" * jogador.cartoes_amarelos
                extras.append(amarelos)

            if extras:
                texto += " [" + " ".join(extras) + "]"

            btn = ctk.CTkButton(
                scroll_elenco,
                text=texto,
                anchor="w",
                fg_color="transparent",
                text_color=cor_texto,
                border_width=1,
                border_color="gray",
                command=lambda j=jogador: self.abrir_detalhes(j)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def montar_aba_tabela(self):
        for widget in self.aba_tabela.winfo_children():
            widget.destroy()

        tabela_atual = self.campeonato.tabela
        classificacao = sorted(tabela_atual.values(), key=lambda p: (p.pontos, p.vitorias, p.saldo_gols()),
                               reverse=True)

        scroll_tabela = ctk.CTkScrollableFrame(self.aba_tabela)
        scroll_tabela.pack(fill="both", expand=True)

        topo = ctk.CTkLabel(scroll_tabela, text=f"{'Time':<20} {'PTS':<5} {'V':<5} {'E':<5} {'D':<5} {'SG':<5}",
                            font=("Courier", 12, "bold"))
        topo.pack(anchor="w", padx=10)

        for pos in classificacao:
            cor = "yellow" if pos.time == self.campeonato.time_do_usuario else "white"
            txt = f"{pos.time.nome:<20} {pos.pontos:<5} {pos.vitorias:<5} {pos.empates:<5} {pos.derrotas:<5} {pos.saldo_gols():<5}"
            lbl = ctk.CTkLabel(scroll_tabela, text=txt, font=("Courier", 12), text_color=cor, anchor="w")
            lbl.pack(anchor="w", padx=10)

    def montar_aba_calendario(self):
        for widget in self.aba_jogos.winfo_children():
            widget.destroy()

        data_str = self.campeonato.data_atual.strftime("%d/%m/%Y")
        lbl_data = ctk.CTkLabel(self.aba_jogos, text=f"Data Atual: {data_str}", font=("Arial", 16, "bold"))
        lbl_data.pack(pady=5)

        scroll_jogos = ctk.CTkScrollableFrame(self.aba_jogos)
        scroll_jogos.pack(fill="both", expand=True)

        jogos_hoje, num_rodada = self.campeonato.get_jogos_de_hoje()

        if not jogos_hoje:
            lbl = ctk.CTkLabel(scroll_jogos, text="Treino e Recuperação (Sem jogos hoje).")
            lbl.pack(pady=20)
        else:
            lbl_rodada = ctk.CTkLabel(scroll_jogos, text=f"--- RODADA {num_rodada} ---", font=("Arial", 16, "bold"))
            lbl_rodada.pack(pady=5)

            for jogo in jogos_hoje:
                frame_jogo = ctk.CTkFrame(scroll_jogos, fg_color="transparent")
                frame_jogo.pack(fill="x", pady=5, padx=10)

                cor_placar = "white"
                if jogo.time_casa == self.campeonato.time_do_usuario or jogo.time_visitante == self.campeonato.time_do_usuario:
                    cor_placar = "#00FFFF"

                if jogo.foi_jogado:
                    txt_placar = f"{jogo.time_casa.nome} {jogo.placar_casa} x {jogo.placar_visitante} {jogo.time_visitante.nome}"
                    lbl_placar = ctk.CTkLabel(frame_jogo, text=txt_placar, font=("Arial", 14, "bold"),
                                              text_color=cor_placar)
                    lbl_placar.pack()

                    detalhes = []
                    if jogo.autores_casa: detalhes.append(f"{jogo.time_casa.nome}: {', '.join(jogo.autores_casa)}")
                    if jogo.autores_visitante: detalhes.append(
                        f"{jogo.time_visitante.nome}: {', '.join(jogo.autores_visitante)}")
                    if jogo.lesionados: detalhes.append(f"🚑: {', '.join(jogo.lesionados)}")
                    if jogo.cartoes: detalhes.append(f"🟥: {', '.join(jogo.cartoes)}")

                    if detalhes:
                        lbl_detalhes = ctk.CTkLabel(frame_jogo, text=" | ".join(detalhes), font=("Arial", 11),
                                                    text_color="gray")
                        lbl_detalhes.pack()
                else:
                    txt = f"{jogo.time_casa.nome} x {jogo.time_visitante.nome}"
                    lbl = ctk.CTkLabel(frame_jogo, text=txt, font=("Arial", 14), text_color=cor_placar)
                    lbl.pack()

    def montar_aba_mercado(self):
        for widget in self.aba_mercado.winfo_children():
            widget.destroy()

        meu_time = self.campeonato.time_do_usuario
        saldo = meu_time.saldo_em_caixa

        lbl_saldo = ctk.CTkLabel(self.aba_mercado, text=f"SEU SALDO: R$ {saldo:,.2f}", font=("Arial", 20, "bold"),
                                 text_color="green")
        lbl_saldo.pack(pady=10)

        scroll_mercado = ctk.CTkScrollableFrame(self.aba_mercado)
        scroll_mercado.pack(fill="both", expand=True)

        todos_jogadores = []
        for time in self.campeonato.times:
            if time != meu_time:
                todos_jogadores.extend(time.elenco)

        todos_jogadores.sort(key=lambda j: j.valor_mercado, reverse=True)

        for jogador in todos_jogadores[:50]:
            frame_linha = ctk.CTkFrame(scroll_mercado, fg_color="transparent")
            frame_linha.pack(fill="x", pady=2, padx=5)

            txt = f"{jogador.nome} ({jogador.funcao}) - Pot: {jogador.potencial} | R$ {jogador.valor_mercado:,.2f}"

            avisos = []
            if jogador.esta_lesionado: avisos.append("LESIONADO")
            if jogador.suspenso: avisos.append("SUSPENSO")

            if avisos: txt += f" [{' '.join(avisos)}]"

            lbl = ctk.CTkLabel(frame_linha, text=txt, font=("Arial", 12), anchor="w")
            lbl.pack(side="left", padx=10)

            pode_comprar = (saldo >= jogador.valor_mercado) and (not jogador.esta_lesionado) and (not jogador.suspenso)

            cor_btn = "green" if pode_comprar else "gray"
            estado_btn = "normal" if pode_comprar else "disabled"

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

            self.atualizar_interface()

    def abrir_detalhes(self, jogador):
        TelaDetalhesJogador(self, jogador)


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
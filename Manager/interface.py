import customtkinter as ctk
from campeonato import Campeonato
from main import criar_times_da_liga


class Interface:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Python Football Manager 2026")
        self.root.geometry("1000x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.tela_inicial()

    def tela_inicial(self):
        self.frame_inicial = ctk.CTkFrame(self.root)
        self.frame_inicial.pack(fill="both", expand=True)

        lbl_titulo = ctk.CTkLabel(self.frame_inicial, text="Python Football Manager", font=("Arial", 32, "bold"))
        lbl_titulo.pack(pady=50)

        btn_novo_jogo = ctk.CTkButton(self.frame_inicial, text="Iniciar Novo Jogo", command=self.iniciar_jogo,
                                      width=200, height=50)
        btn_novo_jogo.pack(pady=20)

    def iniciar_jogo(self):
        times = criar_times_da_liga()
        self.campeonato = Campeonato(times, 2025)

        print(f"Jogo criado! Técnico do: {self.campeonato.time_do_usuario.nome}")

        self.frame_inicial.destroy()
        self.abrir_dashboard()

    def abrir_dashboard(self):
        self.abas = ctk.CTkTabview(self.root)
        self.abas.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_elenco = self.abas.add("Meu Elenco")
        self.aba_tabela = self.abas.add("Classificação")
        self.aba_jogos = self.abas.add("Calendário")
        self.aba_mercado = self.abas.add("Mercado")

        self.montar_aba_elenco()
        self.montar_aba_tabela()
        self.montar_aba_calendario()
        self.montar_aba_mercado()

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

            cor_texto = "red" if jogador.esta_lesionado else ("gray10", "gray90")

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

        tabela_atual = self.campeonato.tabela.posicoes
        classificacao = sorted(tabela_atual.values(), key=lambda p: (p.pontos, p.vitorias, p.saldo_gols()),
                               reverse=True)

        scroll_tabela = ctk.CTkScrollableFrame(self.aba_tabela)
        scroll_tabela.pack(fill="both", expand=True)

        topo = ctk.CTkLabel(scroll_tabela, text=f"{'Time':<20} {'PTS':<5} {'V':<5} {'E':<5} {'D':<5} {'SG':<5}",
                            font=("Courier", 12, "bold"))
        topo.pack(anchor="w", padx=10)

        for pos in classificacao:
            txt = f"{pos.time.nome:<20} {pos.pontos:<5} {pos.vitorias:<5} {pos.empates:<5} {pos.derrotas:<5} {pos.saldo_gols():<5}"
            lbl = ctk.CTkLabel(scroll_tabela, text=txt, font=("Courier", 12), anchor="w")
            lbl.pack(anchor="w", padx=10)

    def montar_aba_calendario(self):
        for widget in self.aba_jogos.winfo_children():
            widget.destroy()

        data_str = self.campeonato.data_atual.strftime("%d/%m/%Y")
        btn_avancar = ctk.CTkButton(self.aba_jogos, text=f"Avançar Dia ({data_str})", command=self.avancar_dia,
                                    fg_color="green")
        btn_avancar.pack(pady=10)

        scroll_jogos = ctk.CTkScrollableFrame(self.aba_jogos)
        scroll_jogos.pack(fill="both", expand=True)

        jogos_hoje = self.campeonato.get_jogos_de_hoje()

        if not jogos_hoje:
            lbl = ctk.CTkLabel(scroll_jogos, text="Nenhum jogo agendado para hoje.")
            lbl.pack(pady=20)
        else:
            for jogo in jogos_hoje:
                if jogo.foi_jogado:
                    txt = f"{jogo.time_casa.nome} {jogo.placar_casa} x {jogo.placar_visitante} {jogo.time_visitante.nome}"
                else:
                    txt = f"{jogo.time_casa.nome} x {jogo.time_visitante.nome}"

                lbl = ctk.CTkLabel(scroll_jogos, text=txt, font=("Arial", 14))
                lbl.pack(pady=5)

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

            self.atualizar_interface()

    def avancar_dia(self):
        self.campeonato.avancar_um_dia()
        self.atualizar_interface()

    def atualizar_interface(self):
        self.montar_aba_elenco()
        self.montar_aba_tabela()
        self.montar_aba_calendario()
        self.montar_aba_mercado()

    def abrir_detalhes(self, jogador):
        janela = ctk.CTkToplevel(self.root)
        janela.title(f"Detalhes: {jogador.nome}")
        janela.geometry("400x450")

        janela.attributes("-topmost", True)

        lbl_nome = ctk.CTkLabel(janela, text=jogador.nome, font=("Arial", 22, "bold"))
        lbl_nome.pack(pady=(20, 5))

        lbl_funcao = ctk.CTkLabel(janela, text=f"{jogador.funcao} | {jogador.nacionalidade}", text_color="gray")
        lbl_funcao.pack(pady=0)

        frame_infos = ctk.CTkFrame(janela)
        frame_infos.pack(pady=20, padx=20, fill="x")

        def criar_linha(titulo, valor, cor="white"):
            f = ctk.CTkFrame(frame_infos, fg_color="transparent")
            f.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(f, text=titulo, text_color="gray").pack(side="left")
            ctk.CTkLabel(f, text=valor, text_color=cor, font=("Arial", 12, "bold")).pack(side="right")

        idade = 2025 - jogador.data_nascimento.year

        criar_linha("Idade:", f"{idade} anos")
        criar_linha("Potencial:", f"{jogador.potencial}")
        criar_linha("Condição Física:", f"{jogador.condicao_fisica}%",
                    "green" if jogador.condicao_fisica > 80 else "red")

        ctk.CTkFrame(janela, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=10)

        lbl_financas = ctk.CTkLabel(janela, text="FINANÇAS", font=("Arial", 14, "bold"))
        lbl_financas.pack(pady=5)

        lbl_salario = ctk.CTkLabel(janela, text=f"Salário: R$ {jogador.salario:,.2f} / semana", text_color="yellow")
        lbl_salario.pack()

        lbl_valor = ctk.CTkLabel(janela, text=f"Valor de Mercado: R$ {jogador.valor_mercado:,.2f}",
                                 text_color="#00FF00")
        lbl_valor.pack()

        btn_vender = ctk.CTkButton(
            janela,
            text="VENDER JOGADOR",
            fg_color="red",
            hover_color="darkred",
            command=lambda: [self.vender_jogador(jogador), janela.destroy()]
        )
        btn_vender.pack(pady=30, padx=40, fill="x")

    def vender_jogador(self, jogador):
        meu_time = self.campeonato.time_do_usuario
        valor_venda = jogador.valor_mercado

        if jogador in meu_time.elenco:
            meu_time.elenco.remove(jogador)

            meu_time.saldo_em_caixa += valor_venda

            print(f"💰 VENDIDO! {jogador.nome} saiu por R$ {valor_venda:,.2f}")

            self.atualizar_interface()


if __name__ == "__main__":
    app = Interface()
    app.root.mainloop()
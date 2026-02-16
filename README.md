# ⚽ Python Football Manager 2026

Um simulador de gestão de futebol desenvolvido em Python, focado na aplicação de conceitos de Engenharia de Software, Orientação a Objetos e Algoritmos de Simulação.

![Status](https://img.shields.io/badge/Status-Versão%201.0%20(Estável)-green)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Interface](https://img.shields.io/badge/Interface-CustomTkinter-purple)

## 📋 Sobre o Projeto

Este projeto é um estudo prático sobre como construir sistemas complexos e interligados. O objetivo foi recriar a lógica de um jogo "Manager" onde o usuário não controla os jogadores em campo, mas sim toma as decisões administrativas e táticas que definem o sucesso do clube.

### ✅ Funcionalidades Implementadas (Versão 1.0)

* **Motor de Jogo Estatístico:** As partidas não são decididas na sorte. Um algoritmo compara a força de ataque vs defesa dos times para gerar probabilidades reais de gol.
* **Economia Viva:**
    * Jogadores têm valor de mercado dinâmico (baseado em idade e potencial).
    * Salários são pagos semanalmente, exigindo gestão de caixa.
    * Receita de bilheteria nos jogos em casa.
* **Mercado de Transferências:** É possível navegar pelos elencos rivais e comprar jogadores, impactando o orçamento.
* **Calendário Round-Robin:** Um algoritmo gera automaticamente um campeonato de pontos corridos (todos contra todos, turno e returno) sem conflitos de data.
* **Gestão de Elenco:**
    * Visualização detalhada de atributos.
    * Histórico de gols na temporada.
    * Sistema de Lesões (tempo de recuperação) e Cartões (suspensão automática).
* **Interface Gráfica:** Dashboard moderno com abas, modo escuro e navegação fluida.
* **Sistema de Save/Load:** Persistência de dados completa usando serialização de objetos.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Interface:** `customtkinter` (GUI moderna)
* **Persistência:** Biblioteca `pickle`
* **Conceitos de POO:** Classes, Herança, Encapsulamento, Composição e Polimorfismo.

## 🚀 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone (https://github.com/Wes2601/Manager.git)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install customtkinter
    ```
3.  **Rode o jogo:**
    ```bash
    python interface.py
    ```

## 🔜 Próximos Passos (Roadmap)

* [ ] Implementar sistema de Táticas (Formações 4-4-2, 4-3-3).
* [ ] Adicionar Inteligência Artificial para os times rivais contratarem jogadores.
* [ ] Criar sistema de categorias de base.

---
**Desenvolvido por [Wesley de Moura Brito]**
**Link do projeto: (https://github.com/Wes2601/Manager)**
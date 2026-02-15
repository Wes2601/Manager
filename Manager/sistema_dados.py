import pickle
import os

ARQUIVO_SAVE = "savegame.dat"

def salvar_jogo(campeonato):

    try:
        with open(ARQUIVO_SAVE, "wb") as arquivo:
            pickle.dump(campeonato, arquivo)
        print("Jogo salvo com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    return False

def carregar_jogo():
    if not(os.path.exists(ARQUIVO_SAVE)):
        return None

    try:
        with open(ARQUIVO_SAVE, "rb") as arquivo:
            campeonato = pickle.load(arquivo)
        print("Jogo carregado com sucesso!")
        return campeonato
    except Exception as e:
        print(f"Erro ao carregar: {e}")
        return None

def existe_save():
    return os.path.exists(ARQUIVO_SAVE)

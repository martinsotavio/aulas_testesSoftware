from app import regras

SUBSTITUI = ["validar_titulo"]


def validar_titulo(tipo, descricao, valor):
    if tipo not in regras.TIPOS:
        raise regras.RegraVioladaError("O tipo deve ser pagar ou receber.")
    if not descricao.strip():
        raise regras.RegraVioladaError("A descrição é obrigatória.")
    if valor < 0:
        raise regras.RegraVioladaError("O valor do título deve ser maior que zero.")

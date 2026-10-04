from app import regras

SUBSTITUI = ["validar_baixa"]


def validar_baixa(saldo, status, valor):
    if status == "cancelado":
        raise regras.RegraVioladaError(f"Título {status} não pode receber baixa.")
    if valor <= 0:
        raise regras.RegraVioladaError("O valor da baixa deve ser maior que zero.")
    if valor > saldo:
        raise regras.RegraVioladaError("O valor da baixa não pode ser maior que o saldo do título.")

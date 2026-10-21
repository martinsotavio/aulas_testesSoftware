SUBSTITUI = ["novo_status"]


def novo_status(valor_do_titulo, saldo_restante):
    if saldo_restante < 0:
        return "quitado"
    if saldo_restante < valor_do_titulo:
        return "parcial"
    return "aberto"

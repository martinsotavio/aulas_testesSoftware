from decimal import ROUND_HALF_UP

from app import regras

SUBSTITUI = ["gerar_parcelas"]


def gerar_parcelas(valor, quantidade):
    if quantidade < 1:
        raise regras.RegraVioladaError("A quantidade de parcelas deve ser pelo menos 1.")
    parcela = (valor / quantidade).quantize(regras.CENTAVO, rounding=ROUND_HALF_UP)
    return [parcela] * quantidade

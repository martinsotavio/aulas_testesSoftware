from decimal import ROUND_DOWN, ROUND_HALF_UP

from app import regras

SUBSTITUI = ["calcular_encargos"]


def calcular_encargos(valor, vencimento, pagamento):
    vencimento_efetivo = regras.proximo_dia_util(vencimento)
    if pagamento < vencimento_efetivo:
        return regras.ZERO
    dias_de_atraso = (pagamento - vencimento_efetivo).days
    encargos = valor * regras.MULTA + valor * regras.JUROS_AO_DIA * dias_de_atraso
    return encargos.quantize(regras.CENTAVO, rounding=ROUND_HALF_UP)

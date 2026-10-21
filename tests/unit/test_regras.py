from datetime import date
from decimal import Decimal

import pytest

from app.regras import (
    RegraVioladaError,
    calcular_encargos,
    gerar_parcelas,
    validar_baixa,
    validar_titulo,
)


def test_um_dia_de_atraso_paga_multa_mais_um_dia_de_juros():
    valor = Decimal("1000.00")
    vencimento = date(2026, 11, 10)           # terça-feira

    encargos = calcular_encargos(valor, vencimento, pagamento=date(2026, 11, 11))

    assert encargos == Decimal("20.33")       # multa 20,00 + juros de um dia 0,33


def test_parcelamento_em_zero_vezes_e_rejeitado():
    with pytest.raises(RegraVioladaError):
        gerar_parcelas(Decimal("100.00"), 0)


# Casos da planilha (docs/casos_de_teste.csv). Os que falham documentam defeitos.

def test_pagamento_no_dia_do_vencimento_nao_tem_encargos():           # CT07
    vencimento = date(2026, 11, 10)

    encargos = calcular_encargos(Decimal("1000.00"), vencimento, pagamento=vencimento)

    assert encargos == Decimal("0.00")


def test_trinta_dias_de_atraso_pagam_multa_mais_trinta_dias_de_juros():  # CT09
    vencimento = date(2026, 11, 10)

    encargos = calcular_encargos(Decimal("1000.00"), vencimento, pagamento=date(2026, 12, 10))

    assert encargos == Decimal("29.90")


def test_vencimento_no_sabado_pago_na_segunda_nao_tem_encargos():     # CT10
    sabado = date(2026, 10, 10)

    encargos = calcular_encargos(Decimal("1000.00"), sabado, pagamento=date(2026, 10, 12))

    assert encargos == Decimal("0.00")


def test_centavos_que_sobram_do_parcelamento_vao_para_a_primeira_parcela():  # CT06
    parcelas = gerar_parcelas(Decimal("100.00"), 3)

    assert parcelas == [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")]


def test_titulo_com_valor_zero_e_rejeitado():                         # CT02
    with pytest.raises(RegraVioladaError):
        validar_titulo("pagar", "Valor zero", Decimal("0.00"))


def test_titulo_com_valor_negativo_e_rejeitado():                     # CT03
    with pytest.raises(RegraVioladaError):
        validar_titulo("pagar", "Valor negativo", Decimal("-50.00"))


def test_titulo_sem_descricao_e_rejeitado():                          # CT04
    with pytest.raises(RegraVioladaError):
        validar_titulo("pagar", "   ", Decimal("10.00"))


def test_baixa_maior_que_o_saldo_e_rejeitada():                       # CT12
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("600.00"), status="parcial", valor=Decimal("700.00"))


def test_baixa_de_valor_zero_e_rejeitada():                           # CT13
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("100.00"), status="aberto", valor=Decimal("0.00"))


def test_titulo_quitado_nao_recebe_baixa():                           # CT14
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("0.00"), status="quitado", valor=Decimal("10.00"))


def test_titulo_cancelado_nao_recebe_baixa():                         # CT15
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("100.00"), status="cancelado", valor=Decimal("50.00"))

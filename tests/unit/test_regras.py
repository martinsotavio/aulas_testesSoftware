"""Testes unitários das regras de negócio (docs/regras_de_negocio.md).

Os valores esperados foram calculados à mão a partir da especificação.
"""
from datetime import date
from decimal import Decimal

import pytest

from app.regras import (
    RegraVioladaError,
    calcular_encargos,
    gerar_parcelas,
    novo_status,
    proximo_dia_util,
    validar_baixa,
    validar_titulo,
    vencimentos_das_parcelas,
)

VENCIMENTO = date(2026, 11, 10)   # terça-feira


# Regra 5: vencimento em fim de semana

@pytest.mark.parametrize("data, esperado", [
    (date(2026, 10, 10), date(2026, 10, 12)),   # sábado -> segunda
    (date(2026, 10, 11), date(2026, 10, 12)),   # domingo -> segunda
])
def test_fim_de_semana_e_prorrogado_para_segunda(data, esperado):
    resultado = proximo_dia_util(data)

    assert resultado == esperado


@pytest.mark.parametrize("dia_util", [
    date(2026, 10, 9),    # sexta
    date(2026, 10, 12),   # segunda
])
def test_dia_util_nao_muda(dia_util):
    resultado = proximo_dia_util(dia_util)

    assert resultado == dia_util


# Regra 4: encargos por atraso

@pytest.mark.parametrize("pagamento, esperado", [
    (date(2026, 10, 1), Decimal("0.00")),    # bem antes do vencimento
    (date(2026, 11, 9), Decimal("0.00")),    # véspera do vencimento
    (date(2026, 11, 10), Decimal("0.00")),   # no dia do vencimento
    (date(2026, 11, 11), Decimal("20.33")),  # 1 dia: 20,00 + 0,33
    (date(2026, 11, 20), Decimal("23.30")),  # 10 dias: 20,00 + 3,30
    (date(2026, 12, 10), Decimal("29.90")),  # 30 dias: 20,00 + 9,90
])
def test_encargos_sobre_titulo_de_mil_reais(pagamento, esperado):
    valor = Decimal("1000.00")

    encargos = calcular_encargos(valor, VENCIMENTO, pagamento)

    assert encargos == esperado


@pytest.mark.parametrize("valor, pagamento, esperado", [
    ("150.00", date(2026, 11, 11), "3.05"),   # 3,00 + 0,0495 = 3,0495
    ("150.00", date(2026, 12, 10), "4.49"),   # 3,00 + 1,485 = 4,485: meio centavo para cima
    ("333.33", date(2026, 11, 11), "6.78"),   # 6,6666 + 0,1099989 = 6,7765989
    ("0.01", date(2026, 11, 10), "0.00"),     # no dia do vencimento, mesmo com valor mínimo
])
def test_encargos_com_valores_quebrados(valor, pagamento, esperado):
    encargos = calcular_encargos(Decimal(valor), VENCIMENTO, pagamento)

    assert encargos == Decimal(esperado)


@pytest.mark.parametrize("pagamento, esperado", [
    (date(2026, 11, 13), Decimal("0.00")),   # sexta, antes do vencimento
    (date(2026, 11, 15), Decimal("0.00")),   # domingo, ainda antes da data prorrogada
    (date(2026, 11, 16), Decimal("0.00")),   # segunda: a data prorrogada
    (date(2026, 11, 17), Decimal("20.33")),  # terça: 1 dia depois da data prorrogada
])
def test_encargos_com_vencimento_no_sabado(pagamento, esperado):
    sabado = date(2026, 11, 14)

    encargos = calcular_encargos(Decimal("1000.00"), sabado, pagamento)

    assert encargos == esperado


def test_vencimento_no_domingo_pago_na_segunda_nao_tem_encargos():
    domingo = date(2026, 11, 15)

    encargos = calcular_encargos(Decimal("1000.00"), domingo, pagamento=date(2026, 11, 16))

    assert encargos == Decimal("0.00")


# Regra 6: parcelamento

@pytest.mark.parametrize("valor, quantidade, esperado", [
    ("100.00", 1, ["100.00"]),
    ("100.00", 3, ["33.34", "33.33", "33.33"]),
    ("100.00", 6, ["16.70", "16.66", "16.66", "16.66", "16.66", "16.66"]),
    ("333.33", 2, ["166.67", "166.66"]),
    ("0.10", 3, ["0.04", "0.03", "0.03"]),
    ("1000.00", 4, ["250.00", "250.00", "250.00", "250.00"]),
])
def test_parcelas_com_resto_na_primeira(valor, quantidade, esperado):
    parcelas = gerar_parcelas(Decimal(valor), quantidade)

    assert parcelas == [Decimal(p) for p in esperado]


def test_soma_das_parcelas_e_exatamente_o_valor_original():
    parcelas = gerar_parcelas(Decimal("1000.00"), 7)

    assert sum(parcelas) == Decimal("1000.00")


@pytest.mark.parametrize("quantidade", [0, -1])
def test_quantidade_de_parcelas_invalida_e_rejeitada(quantidade):
    with pytest.raises(RegraVioladaError):
        gerar_parcelas(Decimal("100.00"), quantidade)


def test_parcelas_vencem_de_30_em_30_dias():
    vencimentos = vencimentos_das_parcelas(VENCIMENTO, 3)

    assert vencimentos == [date(2026, 11, 10), date(2026, 12, 10), date(2027, 1, 9)]


# Regra 1: validação do título

@pytest.mark.parametrize("valor", ["0.00", "-0.01", "-50.00"])
def test_titulo_com_valor_zero_ou_negativo_e_rejeitado(valor):
    with pytest.raises(RegraVioladaError):
        validar_titulo("pagar", "Aluguel", Decimal(valor))


def test_tipo_desconhecido_e_rejeitado_com_mensagem_clara():
    with pytest.raises(RegraVioladaError, match="pagar"):
        validar_titulo("emprestar", "Aluguel", Decimal("10.00"))


@pytest.mark.parametrize("descricao", ["", "   "])
def test_titulo_sem_descricao_e_rejeitado(descricao):
    with pytest.raises(RegraVioladaError, match="descrição"):
        validar_titulo("pagar", descricao, Decimal("10.00"))


@pytest.mark.parametrize("tipo", ["pagar", "receber"])
def test_titulo_valido_de_um_centavo_e_aceito(tipo):
    validar_titulo(tipo, "Mensalidade", Decimal("0.01"))


# Regra 3: validação da baixa

@pytest.mark.parametrize("status", ["aberto", "parcial"])
def test_baixa_igual_ao_saldo_e_aceita(status):
    validar_baixa(saldo=Decimal("100.00"), status=status, valor=Decimal("100.00"))


def test_baixa_de_um_centavo_e_aceita():
    validar_baixa(saldo=Decimal("100.00"), status="aberto", valor=Decimal("0.01"))


def test_baixa_um_centavo_acima_do_saldo_e_rejeitada():
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("100.00"), status="aberto", valor=Decimal("100.01"))


@pytest.mark.parametrize("valor", ["0.00", "-10.00"])
def test_baixa_de_valor_zero_ou_negativo_e_rejeitada(valor):
    with pytest.raises(RegraVioladaError):
        validar_baixa(saldo=Decimal("100.00"), status="aberto", valor=Decimal(valor))


@pytest.mark.parametrize("status, saldo", [
    ("cancelado", "100.00"),
    ("quitado", "0.00"),
])
def test_titulo_cancelado_ou_quitado_nao_recebe_baixa(status, saldo):
    with pytest.raises(RegraVioladaError, match=status):
        validar_baixa(saldo=Decimal(saldo), status=status, valor=Decimal("0.01"))


# Regra 2: status depois da baixa

@pytest.mark.parametrize("saldo_restante, esperado", [
    ("100.00", "aberto"),    # nada foi baixado
    ("99.99", "parcial"),    # um centavo baixado
    ("0.01", "parcial"),     # falta um centavo
    ("0.00", "quitado"),
])
def test_novo_status_depois_da_baixa(saldo_restante, esperado):
    status = novo_status(Decimal("100.00"), Decimal(saldo_restante))

    assert status == esperado

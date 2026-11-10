"""Fluxo da baixa, de ponta a ponta, no navegador.

Cada teste começa com o banco vazio (fixture banco_limpo, do conftest) e cria os
próprios dados pela interface. Nada de time.sleep: o expect espera sozinho.
"""
import os

import pytest
from playwright.sync_api import Page, expect

USUARIO = os.environ.get("USUARIO", "admin")
SENHA = os.environ.get("SENHA", "admin123")

VENCIMENTO = "2026-11-10"
PAGAMENTO = "2026-11-05"  # antes do vencimento: sem encargos por atraso


@pytest.fixture
def pagina(page: Page) -> Page:
    """Página já autenticada, na lista de títulos."""
    page.goto("/login")
    page.get_by_label("Usuário").fill(USUARIO)
    page.get_by_label("Senha").fill(SENHA)
    page.get_by_role("button", name="Entrar").click()
    expect(page.get_by_role("heading", name="Títulos")).to_be_visible()
    return page


def cadastrar_titulo_a_receber(pagina: Page, descricao: str, valor: str) -> None:
    pagina.get_by_role("link", name="Novo título").click()
    pagina.get_by_label("Tipo").select_option(label="A receber")
    pagina.get_by_label("Descrição").fill(descricao)
    pagina.get_by_label("Valor").fill(valor)
    pagina.get_by_label("Vencimento").fill(VENCIMENTO)
    pagina.get_by_role("button", name="Salvar").click()
    expect(pagina.get_by_role("status")).to_have_text("Título cadastrado.")


def registrar_baixa(pagina: Page, descricao: str, valor: str) -> None:
    linha = pagina.get_by_role("row").filter(has_text=descricao)
    linha.get_by_role("link", name="Baixar").click()
    pagina.get_by_label("Valor da baixa").fill(valor)
    pagina.get_by_label("Data do pagamento").fill(PAGAMENTO)
    pagina.get_by_role("button", name="Registrar baixa").click()


def test_baixa_parcial_atualiza_saldo_status_e_fluxo_de_caixa(pagina: Page):
    cadastrar_titulo_a_receber(pagina, "Mensalidade", "1000,00")

    registrar_baixa(pagina, "Mensalidade", "400,00")
    expect(pagina.get_by_role("status")).to_contain_text("Baixa registrada")

    # Na lista de títulos
    pagina.get_by_role("link", name="Títulos").click()
    linha = pagina.get_by_role("row").filter(has_text="Mensalidade")
    expect(linha.locator("[data-campo=saldo]")).to_have_text("600.00")
    expect(linha.locator("[data-campo=status]")).to_have_text("parcial")

    # No fluxo de caixa, com um período fixo que contém o vencimento
    pagina.get_by_role("link", name="Fluxo de caixa").click()
    pagina.get_by_label("Início").fill("2026-11-01")
    pagina.get_by_label("Fim").fill("2026-11-30")
    pagina.get_by_role("button", name="Calcular").click()
    expect(pagina.locator("[data-campo=saldo-projetado]")).to_have_text("600.00")


def test_baixa_maior_que_o_saldo_mostra_erro_e_nao_altera_o_saldo(pagina: Page):
    cadastrar_titulo_a_receber(pagina, "Aluguel", "1000,00")

    registrar_baixa(pagina, "Aluguel", "1500,00")

    expect(pagina.get_by_role("alert")).to_have_text(
        "O valor da baixa não pode ser maior que o saldo do título."
    )
    expect(pagina.locator("[data-campo=saldo]")).to_have_text("1000.00")
    expect(pagina.get_by_text("Nenhuma baixa registrada.")).to_be_visible()

    pagina.get_by_role("link", name="Títulos").click()
    linha = pagina.get_by_role("row").filter(has_text="Aluguel")
    expect(linha.locator("[data-campo=saldo]")).to_have_text("1000.00")
    expect(linha.locator("[data-campo=status]")).to_have_text("aberto")

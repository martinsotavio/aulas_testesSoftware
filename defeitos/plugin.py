"""Plugin do pytest usado por validar_testes.py.

Quando a variável de ambiente DEFEITO está definida, troca funções de app.regras
pelas versões defeituosas de defeitos/regras/<DEFEITO>.py antes de os testes
serem carregados.
"""
import importlib
import os


def pytest_configure(config):
    nome = os.environ.get("DEFEITO")
    if not nome:
        return
    defeito = importlib.import_module(f"defeitos.regras.{nome}")
    import app.regras as alvo

    for funcao in defeito.SUBSTITUI:
        setattr(alvo, funcao, getattr(defeito, funcao))

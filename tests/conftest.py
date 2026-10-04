"""Configuração compartilhada dos testes.

Cada teste recebe automaticamente o marcador da pasta em que está
(tests/unit -> unit, tests/banco -> banco, e assim por diante), o que permite
rodar só uma camada: pytest -m unit
"""
from pathlib import Path

import pytest

PASTAS_COM_MARCADOR = ("unit", "banco", "integracao", "e2e", "aceitacao")


def pytest_collection_modifyitems(items):
    raiz = Path(__file__).parent
    for item in items:
        partes = Path(str(item.fspath)).relative_to(raiz).parts
        if partes and partes[0] in PASTAS_COM_MARCADOR:
            item.add_marker(getattr(pytest.mark, partes[0]))

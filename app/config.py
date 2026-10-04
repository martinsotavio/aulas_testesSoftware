"""Configuração lida de variáveis de ambiente.

Os valores padrão servem para rodar fora do Docker, com o banco do Compose
exposto na porta 5433 da máquina.
"""
import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://contas:contas@localhost:5433/contas"
)
DATABASE_URL_TESTE = os.environ.get(
    "DATABASE_URL_TESTE", "postgresql://contas:contas@localhost:5433/contas_teste"
)

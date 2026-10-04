"""Conexão com o PostgreSQL e aplicação das migrações."""
from pathlib import Path

import psycopg

PASTA_MIGRACOES = Path(__file__).resolve().parent.parent / "db" / "migrations"


def aplicar_migracoes(url: str) -> list[str]:
    """Executa, em ordem, os arquivos .sql ainda não aplicados. Devolve os nomes aplicados."""
    aplicadas = []
    with psycopg.connect(url) as conexao:
        conexao.execute(
            "CREATE TABLE IF NOT EXISTS migracoes ("
            "nome text PRIMARY KEY, aplicada_em timestamptz NOT NULL DEFAULT now())"
        )
        ja_aplicadas = {linha[0] for linha in conexao.execute("SELECT nome FROM migracoes")}
        for arquivo in sorted(PASTA_MIGRACOES.glob("*.sql")):
            if arquivo.name in ja_aplicadas:
                continue
            conexao.execute(arquivo.read_text(encoding="utf-8"))
            conexao.execute("INSERT INTO migracoes (nome) VALUES (%s)", (arquivo.name,))
            aplicadas.append(arquivo.name)
    return aplicadas

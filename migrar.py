"""Aplica as migrações de db/migrations nos bancos de desenvolvimento e de teste."""
from app.banco import aplicar_migracoes
from app.config import DATABASE_URL, DATABASE_URL_TESTE

if __name__ == "__main__":
    for nome, url in (("desenvolvimento", DATABASE_URL), ("teste", DATABASE_URL_TESTE)):
        aplicadas = aplicar_migracoes(url)
        print(f"Banco de {nome}: {', '.join(aplicadas) if aplicadas else 'nada a aplicar'}")

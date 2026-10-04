"""Mede a qualidade dos seus testes.

Roda a sua suíte contra versões do sistema com um defeito cada. Um bom conjunto de
testes passa com o código correto e falha com cada versão defeituosa.

    python validar_testes.py            defeitos nas regras (tests/unit)
    python validar_testes.py banco      defeitos nas funções do banco (tests/banco)
"""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PYTEST = [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"]


def suite_passa(pasta: str, defeito: str | None = None) -> bool:
    ambiente = dict(os.environ)
    comando = PYTEST + [pasta]
    if defeito:
        ambiente["DEFEITO"] = defeito
        comando += ["-p", "defeitos.plugin"]
    resultado = subprocess.run(comando, cwd=RAIZ, env=ambiente, capture_output=True, text=True)
    if resultado.returncode not in (0, 1):   # 0 = passou, 1 = algum teste falhou
        print(resultado.stdout[-2000:], resultado.stderr[-2000:])
        sys.exit(f"O pytest não conseguiu rodar {pasta}. Corrija o erro acima.")
    return resultado.returncode == 0


def placar(detectados: list[str], escaparam: list[str]) -> None:
    total = len(detectados) + len(escaparam)
    print(f"\nPlacar: {len(detectados)} de {total} defeitos detectados.")
    if escaparam:
        print("Escaparam dos seus testes:", ", ".join(escaparam))
        print("Abra o arquivo de cada um, descubra o defeito e escreva o teste que o pega.")


def validar_regras() -> None:
    pasta = "tests/unit"
    if not suite_passa(pasta):
        sys.exit("Sua suíte falha com o código atual. Deixe os testes verdes antes de validar.")
    detectados, escaparam = [], []
    for arquivo in sorted((RAIZ / "defeitos" / "regras").glob("d*.py")):
        detectado = not suite_passa(pasta, arquivo.stem)
        print(f"  {arquivo.stem}: {'detectado' if detectado else 'ESCAPOU'}")
        (detectados if detectado else escaparam).append(arquivo.stem)
    placar(detectados, escaparam)


def validar_banco() -> None:
    import psycopg

    from app.config import DATABASE_URL_TESTE

    pasta = "tests/banco"
    funcoes_corretas = (RAIZ / "db" / "migrations" / "003_funcoes.sql").read_text(encoding="utf-8")

    def aplicar(sql: str) -> None:
        with psycopg.connect(DATABASE_URL_TESTE) as conexao:
            conexao.execute(sql)

    if not suite_passa(pasta):
        sys.exit("Sua suíte falha com o banco atual. Deixe os testes verdes antes de validar.")
    detectados, escaparam = [], []
    try:
        for arquivo in sorted((RAIZ / "defeitos" / "banco").glob("b*.sql")):
            aplicar(funcoes_corretas)
            aplicar(arquivo.read_text(encoding="utf-8"))
            detectado = not suite_passa(pasta)
            print(f"  {arquivo.stem}: {'detectado' if detectado else 'ESCAPOU'}")
            (detectados if detectado else escaparam).append(arquivo.stem)
    finally:
        aplicar(funcoes_corretas)
    placar(detectados, escaparam)


if __name__ == "__main__":
    if sys.argv[1:] == ["banco"]:
        validar_banco()
    else:
        validar_regras()

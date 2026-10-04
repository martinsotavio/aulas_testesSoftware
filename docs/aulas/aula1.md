# Aula 1: Caça ao bug e primeiro teste

> Passo a passo para copiar e colar: [`docs/playbooks/aula-1.md`](../playbooks/aula-1.md).

Esta versão da aplicação tem **cinco defeitos** plantados. Seu papel hoje é de testador:
encontrar e documentar, não corrigir.

## 1. Subir o ambiente

```
git clone -o turma -b aula-1 https://github.com/pedromullerupf/teste-software-upf.git
cd teste-software-upf
git switch -c meu-trabalho
docker compose up -d
```

Abra http://localhost:8000.

## 2. Caça ao bug (em duplas)

1. Leia `docs/regras_de_negocio.md`. É a especificação.
2. Use a aplicação tentando quebrar cada regra: valores nas fronteiras, datas no fim de semana, parcelas, baixas parciais, títulos cancelados.
3. Registre cada caso em uma planilha, seguindo `docs/modelo_casos_de_teste.csv`.

## 3. Relato de defeito

Escolha um dos defeitos e escreva um relato completo: título, passos para reproduzir,
resultado esperado, resultado obtido e severidade.

## 4. Do manual ao automatizado

1. Abra `tests/unit/test_exemplo.py` e rode:
   ```
   docker compose run --rm testes pytest -v
   ```
2. Crie `tests/unit/test_regras.py` e transforme dois dos seus casos de teste em funções
   `test_...` que chamam as funções de `app/regras.py`.
3. Rode de novo. Um teste que falha por causa de um defeito é o resultado esperado hoje.

## Para pensar

Quanto tempo levaria repetir todos os seus casos manuais depois de cada mudança no código?

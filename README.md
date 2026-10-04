# Contas a pagar e a receber

Aplicação de estudo da disciplina de Teste de Software (UPF). É pequena de propósito:
o objetivo é testar, não programar.

## Aulas

Cada aula tem uma branch (`aula-1` a `aula-6`) com o projeto como ele deve estar no início daquela aula.
O passo a passo de cada aula, para copiar e colar, está em `docs/playbooks/`, e os exercícios em `docs/aulas/`.
O mapa completo fica na branch `main`: https://github.com/pedromullerupf/teste-software-upf

## Subir o ambiente

Requisitos: Git e Docker (com Docker Compose).

```
docker compose up -d
```

- Aplicação: http://localhost:8000
- PostgreSQL: `localhost:5433`, usuário `contas`, senha `contas`, bancos `contas` (desenvolvimento) e `contas_teste` (testes)

## Rodar os testes

```
docker compose run --rm testes pytest -v
```

Outros comandos úteis:

```
docker compose run --rm testes pytest -m unit          só uma camada
docker compose run --rm testes pytest -k encargos      só testes com "encargos" no nome
docker compose logs -f app                             ver o log da aplicação
docker compose exec db psql -U contas contas           abrir o banco no terminal
docker compose down -v                                 apagar tudo e recomeçar do zero
```

## Onde fica cada coisa

| Caminho | Conteúdo |
|---|---|
| `app/regras.py` | Regras de negócio, em funções puras |
| `app/repositorio.py` | Todo o SQL da aplicação |
| `app/web.py` | Rotas e telas |
| `db/migrations/` | Scripts SQL do banco, aplicados em ordem |
| `tests/` | Testes, separados por camada |
| `docs/regras_de_negocio.md` | O que o sistema deve fazer |
| `docs/aulas/` | Roteiro de cada aula prática |

## Sem Docker

Com Python 3.12 e um PostgreSQL acessível:

```
python -m venv .venv
.venv\Scripts\activate            (Windows)   ou   source .venv/bin/activate   (Linux, macOS)
pip install -r requirements.txt
set DATABASE_URL=postgresql://usuario:senha@servidor:5432/banco            (Windows; no Linux, export)
set DATABASE_URL_TESTE=postgresql://usuario:senha@servidor:5432/banco_teste
python migrar.py
flask --app app.web run --port 8000 --debug
python -m pytest -v
```

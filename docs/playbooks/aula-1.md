# Playbook da aula 1: caça ao bug e primeiro teste

Copie e cole cada bloco, na ordem, em um terminal (PowerShell, Prompt ou Bash).
O roteiro com os exercícios completos está em [`docs/aulas/aula1.md`](../aulas/aula1.md);
este playbook é o caminho guiado até o ambiente funcionando e os primeiros testes rodando.

Requisitos na máquina: **Git** e **Docker** (com Docker Compose).

## 1. Baixar o projeto

```bash
git clone -o turma -b aula-1 https://github.com/pedromullerupf/teste-software-upf.git
cd teste-software-upf
git switch -c meu-trabalho
```

- `-o turma` dá o nome `turma` ao repositório oficial. É dele que você vai buscar a versão de cada aula.
- `meu-trabalho` é a sua branch. Tudo o que você fizer fica nela.

Identifique-se para o Git (troque pelos seus dados):

```bash
git config user.name "Seu Nome"
git config user.email "seu.email@upf.br"
```

## 2. Subir o banco e a aplicação

Na primeira vez o Docker baixa as imagens e instala as dependências. Leva alguns minutos.

```bash
docker compose up -d
docker compose ps
```

Resultado esperado: dois serviços no ar, `db` (com `healthy`) e `app`.

Abra no navegador:

<!-- manual -->
```text
http://localhost:8000
```

Se a página não abrir, veja o que a aplicação está dizendo:

<!-- manual -->
```bash
docker compose logs app
```

## 3. Caça ao bug (em duplas, manual)

1. Leia `docs/regras_de_negocio.md`. É a especificação.
2. Use a aplicação tentando quebrar cada regra. Há **cinco defeitos** plantados.
3. Registre cada caso em uma planilha. Cole isto na primeira linha (ou abra `docs/modelo_casos_de_teste.csv`):

```text
ID;Regra;Pré-condição;Passos;Resultado esperado;Resultado obtido;Passou?
CT01;5;Nenhuma;Calcular o próximo dia útil de 10/10/2026 (sábado);12/10/2026;12/10/2026;Sim
CT02;;;;;;
```

Modelo de relato de defeito:

```text
Título:
Ambiente: versão da aula 1, navegador
Regra relacionada:
Passos para reproduzir:
  1.
  2.
  3.
Resultado esperado:
Resultado obtido:
Severidade (baixa, média, alta):
```

## 4. Rodar o teste que já existe

<!-- contem: 1 passed -->
```bash
docker compose run --rm testes pytest -v
```

Resultado esperado:

```text
tests/unit/test_exemplo.py::test_vencimento_no_sabado_e_prorrogado_para_segunda PASSED
1 passed
```

## 5. Seu primeiro teste

Crie o arquivo `tests/unit/test_regras.py` com este conteúdo:

<!-- arquivo: tests/unit/test_regras.py -->
```python
from datetime import date
from decimal import Decimal

import pytest

from app.regras import RegraVioladaError, calcular_encargos, gerar_parcelas


def test_um_dia_de_atraso_paga_multa_mais_um_dia_de_juros():
    valor = Decimal("1000.00")
    vencimento = date(2026, 11, 10)           # terça-feira

    encargos = calcular_encargos(valor, vencimento, pagamento=date(2026, 11, 11))

    assert encargos == Decimal("20.33")       # multa 20,00 + juros de um dia 0,33


def test_parcelamento_em_zero_vezes_e_rejeitado():
    with pytest.raises(RegraVioladaError):
        gerar_parcelas(Decimal("100.00"), 0)
```

Rode só esse arquivo:

<!-- contem: 2 passed -->
```bash
docker compose run --rm testes pytest -v tests/unit/test_regras.py
```

Resultado esperado: `2 passed`.

## 6. Um teste que encontra um defeito

A especificação diz que pagamento **no dia** do vencimento não tem encargos (regra 4).
Acrescente este teste ao fim de `tests/unit/test_regras.py`:

<!-- acrescentar: tests/unit/test_regras.py -->
```python
def test_pagamento_no_dia_do_vencimento_nao_tem_encargos():
    vencimento = date(2026, 11, 10)

    encargos = calcular_encargos(Decimal("1000.00"), vencimento, pagamento=vencimento)

    assert encargos == Decimal("0.00")
```

Rode só os testes com "encargos" ou "vencimento" no nome:

<!-- espera: falha -->
<!-- contem: 1 failed -->
<!-- contem: assert Decimal('20.00') == Decimal('0.00') -->
```bash
docker compose run --rm testes pytest -v -k "encargos or vencimento"
```

Resultado esperado: **o teste novo falha**. Hoje isso é um bom resultado: ele documenta um defeito.

```text
E       AssertionError: assert Decimal('20.00') == Decimal('0.00')
1 failed, 1 passed, 2 deselected
```

Agora é com você: transforme em testes outros casos da sua planilha. Não corrija `app/regras.py` hoje.

## 7. Guardar o trabalho e encerrar

```bash
git add -A
git commit -m "Aula 1: primeiros testes"
```

Para liberar a máquina sem perder os dados do banco:

```bash
docker compose stop
```

Na próxima aula, na mesma máquina, a pasta e a branch `meu-trabalho` estarão do jeito que você deixou.

### Opcional (recomendado): cópia do seu trabalho no seu GitHub

Se a máquina do laboratório for apagada, o commit local se perde. Crie um repositório **vazio**
na sua conta do GitHub e envie a sua branch (troque o endereço):

<!-- manual -->
```bash
git remote add meu https://github.com/SEU-USUARIO/contas-upf.git
git push -u meu meu-trabalho
```

## Se algo der errado

| Sintoma | O que fazer |
|---|---|
| `port is already allocated` na porta 8000 ou 5433 | Outro programa usa a porta. Feche-o, ou rode `docker compose down` na pasta de outro projeto que esteja no ar |
| A página não abre logo depois do `up` | Espere alguns segundos e recarregue. `docker compose logs app` mostra o andamento |
| Quer recomeçar do zero, apagando os dados | `docker compose down -v` e depois `docker compose up -d` |

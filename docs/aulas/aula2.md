# Aula 2: Testes unitários das regras

> Passo a passo para copiar e colar: [`docs/playbooks/aula-2.md`](../playbooks/aula-2.md).

Hoje o alvo é `app/regras.py`. Todos os testes vão em `tests/unit/test_regras.py`.

## Exercício 1: encargos

Escreva testes para `calcular_encargos` no padrão Arrange, Act, Assert:

- pagamento antes do vencimento
- pagamento no dia do vencimento
- um dia de atraso
- vários dias de atraso
- vencimento no sábado, pagamento na segunda-feira e na terça-feira

Use os exemplos de `docs/regras_de_negocio.md` para saber os valores esperados.

## Exercício 2: parametrize

Reescreva os casos do exercício 1 com `@pytest.mark.parametrize`.
Acrescente pelo menos um caso com valor "quebrado", como 150,00 ou 333,33.

## Exercício 3: parcelas e exceções

Teste `gerar_parcelas`: soma exata, resto na primeira parcela, uma parcela, e zero
parcelas (use `pytest.raises`). Depois teste `validar_titulo` e `validar_baixa`.

## Exercício 4: corrigir e medir

1. Corrija em `app/regras.py` os defeitos que seus testes apontam, até a suíte ficar verde.
2. Meça a qualidade dos seus testes:
   ```
   docker compose run --rm testes python validar_testes.py
   ```
3. Para cada defeito que escapou, abra o arquivo em `defeitos/regras/`, entenda o defeito
   e escreva o teste que faltava.

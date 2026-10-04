# Regras de negócio

Esta é a especificação do sistema. Quando o comportamento da aplicação for diferente
do que está escrito aqui, há um defeito.

## Conceitos

- **Título**: uma conta a pagar ou a receber, com descrição, pessoa (fornecedor ou cliente), valor e vencimento.
- **Baixa**: o registro de um pagamento ou recebimento, total ou parcial, de um título.
- **Saldo**: valor do título menos a soma das baixas.

## Regras

1. **Valor do título.** Deve ser maior que zero. O tipo é `pagar` ou `receber` e a descrição é obrigatória.
2. **Status.** `aberto` (sem baixas), `parcial` (com baixas e saldo maior que zero), `quitado` (saldo zero) e `cancelado`.
3. **Baixa.** O valor da baixa deve ser maior que zero e não pode ser maior que o saldo. Título cancelado ou quitado não recebe baixa.
4. **Encargos por atraso.** Pagamento feito depois do vencimento paga, sobre o valor da baixa, multa de 2% mais juros de 0,033% por dia de atraso. O total é arredondado para duas casas, com meio centavo para cima. Pagamento até o dia do vencimento, inclusive, não tem encargos.
5. **Vencimento em fim de semana.** Vencimento em sábado ou domingo é prorrogado para a segunda-feira seguinte. Os dias de atraso são contados a partir da data prorrogada.
6. **Parcelamento.** Um título pode ser cadastrado em N parcelas (N maior ou igual a 1), que vencem de 30 em 30 dias. A soma das parcelas é exatamente o valor original; os centavos que sobram da divisão vão para a primeira parcela. Exemplo: 100,00 em 3 vezes resulta em 33,34, 33,33 e 33,33.
7. **Fluxo de caixa.** O saldo projetado de um período é o total a receber menos o total a pagar, considerando os saldos dos títulos abertos ou parciais com vencimento no período. (Disponível a partir da aula 4.)
8. **Dinheiro.** Valores monetários usam `Decimal` no Python e `numeric(12,2)` no banco, nunca ponto flutuante.

## Exemplos de encargos

Título de 1.000,00 com vencimento em 10/11/2026 (terça-feira), pago integralmente:

| Data do pagamento | Dias de atraso | Encargos |
|---|---|---|
| 10/11/2026 | 0 | 0,00 |
| 11/11/2026 | 1 | 20,33 |
| 10/12/2026 | 30 | 29,90 |

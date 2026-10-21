# Relato de defeito

**Título:** Pagamento no dia do vencimento é cobrado com multa de 2% na tela de baixa

**Ambiente:** versão da aula 1 (branch `aula-1`, commit 11bfccd), aplicação em http://localhost:8000 via `docker compose up -d`, navegador

**Regra relacionada:** 4 (Encargos por atraso). "Pagamento até o dia do vencimento, inclusive, não tem encargos." Também afeta a regra 5 (vencimento prorrogado do fim de semana).

**Passos para reproduzir:**

1. Abrir http://localhost:8000 e clicar em novo título.
2. Cadastrar: tipo "A pagar", descrição "Enc dia", pessoa "Teste", valor `1000,00`, vencimento `10/11/2026` (terça-feira), parcelas `1`.
3. Na lista, abrir a tela de baixa do título criado.
4. Informar valor `1000,00` e data de pagamento `10/11/2026` (o próprio dia do vencimento) e confirmar.

**Resultado esperado:** mensagem "Baixa registrada. Encargos por atraso: R$ 0.00." e encargos de 0,00 gravados na baixa (regra 4; tabela de exemplos de `docs/regras_de_negocio.md`, linha 10/11/2026 → 0,00).

**Resultado obtido:** mensagem "Baixa registrada. Encargos por atraso: R$ 20.00." e encargos de 20,00 gravados na baixa (multa de 2% com 0 dias de juros).

O mesmo acontece com vencimento em sábado, 10/10/2026, pago na segunda-feira, 12/10/2026 (data prorrogada pela regra 5): encargos de 20,00, quando o esperado é 0,00.

**Severidade:** alta. A cobrança indevida aparece no caso mais comum (pagar em dia), afeta todo título pago no vencimento e grava o valor errado no banco.

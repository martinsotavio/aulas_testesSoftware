-- Executado uma única vez, quando o volume do Postgres é criado.
-- Banco separado para os testes automatizados: nunca teste no banco de desenvolvimento.
CREATE DATABASE contas_teste OWNER contas;

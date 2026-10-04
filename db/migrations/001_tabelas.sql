CREATE TABLE titulos (
    id          serial PRIMARY KEY,
    tipo        text NOT NULL CHECK (tipo IN ('pagar', 'receber')),
    descricao   text NOT NULL,
    pessoa      text NOT NULL DEFAULT '',
    valor       numeric(12, 2) NOT NULL,
    vencimento  date NOT NULL,
    status      text NOT NULL DEFAULT 'aberto'
                CHECK (status IN ('aberto', 'parcial', 'quitado', 'cancelado')),
    criado_em   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE baixas (
    id          serial PRIMARY KEY,
    titulo_id   integer NOT NULL REFERENCES titulos (id),
    valor       numeric(12, 2) NOT NULL,
    encargos    numeric(12, 2) NOT NULL DEFAULT 0,
    data_baixa  date NOT NULL,
    criado_em   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX baixas_titulo_id_idx ON baixas (titulo_id);

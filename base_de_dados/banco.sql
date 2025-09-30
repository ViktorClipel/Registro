CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS especies (
    id INTEGER PRIMARY KEY,
    id_criador INTEGER,
    nome_popular TEXT NOT NULL,
    classificacao TEXT,
    descricao_fisica TEXT,
    comportamento TEXT,
    populacao_estimada INTEGER DEFAULT 1,
    dados_adicionais TEXT,
    FOREIGN KEY (id_criador) REFERENCES usuarios(id) ON DELETE SET NULL
);
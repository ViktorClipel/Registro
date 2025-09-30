CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS especies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_criador INT,
    nome_popular VARCHAR(100) NOT NULL,
    classificacao VARCHAR(50),
    descricao_fisica TEXT,
    comportamento TEXT,
    populacao_estimada INT DEFAULT 1,
    dados_adicionais TEXT,
    FOREIGN KEY (id_criador) REFERENCES usuarios(id) ON DELETE SET NULL
);
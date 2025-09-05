CREATE SCHEMA login;
CREATE TABLE login."user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
INSERT INTO login."user" (username, email, password_hash, created_at)
VALUES
    ('usuario1', 'usuario1@email.com', 'hash1', NOW()),
    ('usuario2', 'usuario2@email.com', 'hash2', NOW());
    
SELECT * FROM login."user";

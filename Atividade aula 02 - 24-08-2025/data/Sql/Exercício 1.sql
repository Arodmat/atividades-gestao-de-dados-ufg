--Coleta dos dados foi por meio de um arquivo CSV

-- Na fase da coleta, tambem foi criado um json como dicionario.
--Estrutura da tabela

CREATE TABLE pessoa (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    data_nascimento DATE,
    salario DECIMAL(10,2)
);


-- Fase armazenamento: Uma camada prata para tratar parcialmente.
CREATE TABLE staging_pessoa (
    id_pessoa TEXT,
    nome_completo TEXT,
    data_nasc TEXT,
    sallary TEXT,
    carga_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--Fase processamento: Necessário algumas mudanças:
--Transformações necessárias:
--id_pessoa virar id (INT).
--nome_completo virar nome (VARCHAR).
--data_nasc virar data_nascimento (DATE).
--Converter formato brasileiro 28/08/1990 para 1990-08-28.
--sallary virar salario (DECIMAL).
--Substituir vírgula por ponto quando necessário.

select * from staging_pessoa sp 

INSERT INTO pessoa (id, nome, data_nascimento, salario)
SELECT
    CAST(id_pessoa AS INT) AS id,
    nome_completo AS nome,
    CASE
        WHEN data_nasc LIKE '%/%' 
             THEN TO_DATE(data_nasc, 'DD/MM/YYYY')
        ELSE TO_DATE(data_nasc, 'YYYY-MM-DD')
    END AS data_nascimento,
    CAST(REPLACE(sallary, ',', '.') AS DECIMAL(10,2)) AS salario
FROM staging_pessoa;

select * from pessoa p 

--Processamento
-- Linhas onde o salário não é numérico
SELECT *
FROM staging_pessoa
WHERE NOT (sallary ~ '^\d+([.,]\d+)?$');

-- Encontrar IDs duplicados
SELECT id_pessoa, COUNT(*)
FROM staging_pessoa
GROUP BY id_pessoa
HAVING COUNT(*) > 1;

SELECT *
FROM staging_pessoa
WHERE id_pessoa IS NULL
   OR nome_completo IS NULL
   OR data_nasc IS NULL
   OR NOT (sallary ~ '^\d+([.,]\d+)?$')
   OR (data_nasc !~ '^\d{2}/\d{2}/\d{4}$' AND data_nasc !~ '^\d{4}-\d{2}-\d{2}$');


--USO DOS DADOS
-- Listar todas as pessoas com salário acima de 5000
SELECT nome, salario
FROM pessoa
WHERE salario > 5000;

-- Salário médio por década de nascimento
SELECT EXTRACT(YEAR FROM data_nascimento)/10*10 AS decada,
       AVG(salario) AS salario_medio
FROM pessoa
GROUP BY decada
ORDER BY decada;

--Fase de Retençao/Descarte
-- Apagar registros antigos da staging
DELETE FROM staging_pessoa
WHERE carga_timestamp < NOW() - INTERVAL '365 days';





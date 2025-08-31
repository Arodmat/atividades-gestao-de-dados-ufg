--Completude: verificar se campos obrigatórios (nome, data de nascimento, salário) estão preenchidos.
SELECT
    COUNT(*) AS total_registros,
    SUM(CASE WHEN nome_completo IS NULL OR nome_completo = '' THEN 1 ELSE 0 END) AS faltando_nome,
    SUM(CASE WHEN data_nasc IS NULL OR data_nasc = '' THEN 1 ELSE 0 END) AS faltando_data,
    SUM(CASE WHEN sallary IS NULL OR sallary = '' THEN 1 ELSE 0 END) AS faltando_salario
FROM staging_pessoa;

--Unicidade: checar duplicidade de id_pessoa (Fiz no outro sql mas vou fazer aqui também)
SELECT
    COUNT(id_pessoa) AS total_ids,
    COUNT(DISTINCT id_pessoa) AS ids_unicos,
    COUNT(id_pessoa) - COUNT(DISTINCT id_pessoa) AS duplicados
FROM staging_pessoa;


--Consistência (tipos válidos) se os formatos e tipos estão corretos (data realmente é data, salário numérico).
SELECT
    SUM(CASE WHEN sallary ~ '^[0-9]+([.,][0-9]{1,2})?$' THEN 0 ELSE 1 END) AS salario_invalido,
    SUM(CASE WHEN data_nasc ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' OR data_nasc ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' 
             THEN 0 ELSE 1 END) AS data_invalida
FROM staging_pessoa;

--Temporalidade: Se as datas de nascimento fazem sentido (não podem ser futuras ou absurdamente antigas).
SELECT
    SUM(CASE WHEN TO_DATE(data_nasc, 'DD-MM-YYYY') > CURRENT_DATE THEN 1 ELSE 0 END) AS datas_futuras,
    SUM(CASE WHEN TO_DATE(data_nasc, 'DD-MM-YYYY') < '1992-08-19' THEN 1 ELSE 0 END) AS datas_antigas
FROM staging_pessoa;

--Validade: Se valores respeitam regras de negócio (ex.: salário maior que 0).
SELECT
  COUNT(*) AS total_registros,
  COUNT(*) FILTER (WHERE sallary IS NULL OR TRIM(sallary) = '') AS salario_missing,
  COUNT(*) FILTER (WHERE NOT (TRIM(sallary) ~ '^\d+([.,]\d+)?$')) AS salario_nao_numerico,
  COUNT(*) FILTER (
    WHERE (TRIM(sallary) ~ '^\d+([.,]\d+)?$')
      AND (CAST(REPLACE(TRIM(sallary), ',', '.') AS NUMERIC) <= 0)
  ) AS salario_menor_igual_zero
FROM staging_pessoa;


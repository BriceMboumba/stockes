--Création des tables 

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, 
    user_name VARCHAR (50),
    password text
    );

CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY, 
    stock_date text,
    open float4,
    high float4,
    low float4,
    close float4,
    adj_close float4,
    volume integer
    );

CREATE TABLE IF NOT EXISTS prediction (
    id SERIAL PRIMARY KEY, 
    recorded_date date,
    open float4,
    high float4,
    low float4,
    volume integer,
    close_generated float4
    );

CREATE TABLE IF NOT EXISTS IDs (
    user_id integer references users(id),
    prediction_id integer references prediction(id)
    );

-- Avoir tous les droits (lecture et écriture) sur les tables listées ci-dessus en utilisant la base de données 'psc_db' en remote --
GRANT ALL ON users TO psc;
GRANT ALL ON prediction TO psc;
GRANT ALL ON IDs TO psc;

-- drop table if exists users; 

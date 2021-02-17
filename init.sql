\c kafka_sink;
CREATE TABLE IF NOT EXISTS api_price(event jsonb, updated_at timestamptz DEFAULT now());
CREATE TABLE IF NOT EXISTS contract_price(event jsonb, updated_at timestamptz DEFAULT now());
-- INSERT INTO coingecko(event) VALUES('{"yo": 5}');
-- SELECT * FROM coingecko;

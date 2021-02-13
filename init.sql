\c kafka_sink;
CREATE TABLE coingecko(event jsonb, updated_at timestamptz DEFAULT now());
-- INSERT INTO coingecko(event) VALUES('{"yo": 5}');
-- SELECT * FROM coingecko;

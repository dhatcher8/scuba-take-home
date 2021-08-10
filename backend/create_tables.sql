

CREATE TABLE eod_stock_prices (
    id serial PRIMARY KEY,
    symbol TEXT NOT NULL,
    dt DATE NOT NULL,
    price NUMERIC NOT NULL
);


INSERT INTO eod_stock_prices(symbol, dt, price)
VALUES ('XXXXXXXX', '2020-01-01', 0.31),
('XXXXXXXX', '2020-01-02', 0.32),
('YYYYYYYYY', '2020-02-02', 31.77),
('ZZZZZZZZ', '2020-03-03', 102.57),
('FFFFFFFF', '2020-04-04', 1097.02);

SELECT * from eod_stock_prices where symbol = 'XXXXXXXX' and dt = '2020-01-01';
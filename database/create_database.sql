CREATE TABLE capital(
	capital_id SERIAL PRIMARY KEY,
	timestamp timestamp,
	capital int
);

CREATE TABLE openorders(
	order_id bigint NOT NULL,
	trade_id bigint PRIMARY KEY,
	time_stamp timestamp NOT NULL,
	year integer NOT NULL,
	month integer NOT NULL,
	day integer NOT NULL,
	hour integer NOT NULL,
	minute integer NOT NULL,
	ticker varchar(6) NOT NULL,
	buy_price float NOT NULL,
	sell_price float NOT NULL,
	quantity integer NOT NULL,
	order_type varchar(5) NOT NULL, 
	trader_id bigint NOT NULL,
	cost float NOT NULL,
	profit float,
	result varchar(1),
	status boolean
);

CREATE TABLE orders(
	order_id bigint PRIMARY KEY,
	trade_id bigint,
	time_stamp timestamp NOT NULL,
	year integer NOT NULL,
	month integer NOT NULL,
	day integer NOT NULL,
	hour integer NOT NULL,
	minute integer NOT NULL,
	ticker varchar(6) NOT NULL,
	buy_price float NOT NULL,
	sell_price float NOT NULL,
	quantity integer NOT NULL,
	order_type varchar(4) NOT NULL, 
	trader_id bigint NOT NULL,
	cost float NOT NULL,
	foreign key(trade_id) REFERENCES openorders(trade_id)
);

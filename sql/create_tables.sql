--данные агрегированые по паре
drop table if exists exmo_info.ticker;
CREATE TABLE exmo_info.ticker(
   ID serial primary key,
   par_name				VARCHAR(30),
   check_at			TIMESTAMP ,
   update_at		timestamp,
   deal_24h_max				numeric(10,2),
   deal_24h_min				numeric(10,2),
   deal_24h_avg				numeric(10,2),
   deal_last				numeric(10,2),
   vol_24h					numeric(10,2),
   buy_cur_max				numeric(10,2),
   sell_cur_min				numeric(10,2)
);

--данные по текущем ордерам
drop table if exists exmo_info.order_book;
CREATE TABLE exmo_info.order_book(
   ID serial primary key,
   par_name				VARCHAR(30),
   check_at			TIMESTAMP ,
   min_ask			numeric(10,2),
   max_bid			numeric(10,2),
   price			numeric(10,2),
   w_ask_1			numeric(10,2),
   l_ask_1			numeric(10,2),
   w_ask_5			numeric(10,2),
   l_ask_5			numeric(10,2),
   w_ask_10			numeric(10,2),
   l_ask_10			numeric(10,2),
   w_ask_20			numeric(10,2),
   l_ask_20			numeric(10,2),
   w_ask_30			numeric(10,2),
   l_ask_30			numeric(10,2),
   w_ask_40			numeric(10,2),
   l_ask_40			numeric(10,2),
   w_ask_50			numeric(10,2),
   l_ask_50			numeric(10,2),
   w_bid_1			numeric(10,2),
   l_bid_1			numeric(10,2),
   w_bid_5			numeric(10,2),
   l_bid_5			numeric(10,2),
   w_bid_10			numeric(10,2),
   l_bid_10			numeric(10,2),
   w_bid_20			numeric(10,2),
   l_bid_20			numeric(10,2),
   w_bid_30			numeric(10,2),
   l_bid_30			numeric(10,2),
   w_bid_40			numeric(10,2),
   l_bid_40			numeric(10,2),
   w_bid_50			numeric(10,2),
   l_bid_50			numeric(10,2)
);

--тестовая вставка в тикер
select *
from exmo_info.ticker;

insert into exmo_info.ticker (par_name , check_at , update_at , deal_24h_max , deal_24h_min , deal_24h_avg , deal_last , vol_24h , buy_cur_max , sell_cur_min )
VALUES ('ETH_USD','20170808 1540','20170808 154030' , 1.1 , 1.2 , 1.3 , 1.4 , 1.5 , 1.6 , 1.7);

--тестовая вставка в книгу ордеров
select *
from exmo_info.order_book;


insert into exmo_info.order_book (par_name , check_at , min_ask ,max_bid , price , w_ask_1 , l_ask_1 , w_ask_5 , l_ask_5 , w_ask_10, l_ask_10 , w_ask_20,l_ask_20, w_ask_30, l_ask_30, w_ask_40, l_ask_40, w_ask_50, l_ask_50, w_bid_1, l_bid_1,w_bid_5, l_bid_5, w_bid_10, l_bid_10, w_bid_20, l_bid_20, w_bid_30, l_bid_30, w_bid_40,l_bid_40, w_bid_50, l_bid_50)
VALUES ('ETH_USD','20180611 230044',530.99734085,529,529.998670425,530.998781558,2,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,528.158880091,3,528.158880091,3,528.158880091,3,525.974009796,17,525.974009796,17,523.723730755,19,523.723730755,19)
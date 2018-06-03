--данные агрегированые по паре
drop table if exists exmo_info.ticker;
CREATE TABLE exmo_info.ticker(
   ID serial primary key,
   par_name          VARCHAR(30),
   check_at       TIMESTAMP ,
   update_at      timestamp,
   deal_24h_max            numeric(10,2),
   deal_24h_min            numeric(10,2),
   deal_24h_avg            numeric(10,2),
   deal_last            numeric(10,2),
   vol_24h              numeric(10,2),
   buy_cur_max          numeric(10,2),
   sell_cur_min            numeric(10,2)
);

--данные по текущем ордерам
drop table if exists exmo_info.order_book;
CREATE TABLE exmo_info.order_book(
   ID serial primary key,
   par_name          VARCHAR(30),
   check_at       TIMESTAMP ,
   --общие данные
   ask_quant         numeric(10,2),
   ask_amount     numeric(10,2),
   ask_top        numeric(10,2),
   bid_quant         numeric(10,2),
   bid_amount     numeric(10,2),
   bid_top        numeric(10,2),
   --средние цены желания купить по количеству
   bid_1q_price      numeric(10,2),
   bid_2q_price      numeric(10,2),
   bid_3q_price      numeric(10,2),
   bid_4q_price      numeric(10,2),
   bid_5q_price      numeric(10,2),
   bid_10q_price     numeric(10,2),
   --цены, количества, количества до линий поддержки
   bid_1l_price            numeric(10,2),
   bid_1l_quant            numeric(10,2),
   bid_1l_before_quant     numeric(10,2),
   bid_2l_price            numeric(10,2),
   bid_2l_quant            numeric(10,2),
   bid_2l_before_quant     numeric(10,2),
   bid_3l_price            numeric(10,2),
   bid_3l_quant            numeric(10,2),
   bid_3l_before_quant     numeric(10,2),
   --средние цены желания продать по количеству
   ask_1q_price      numeric(10,2),
   ask_2q_price      numeric(10,2),
   ask_3q_price      numeric(10,2),
   ask_4q_price      numeric(10,2),
   ask_5q_price      numeric(10,2),
   ask_10q_price     numeric(10,2),
   --цены, количества, количества до линий поддержки
   ask_1l_price            numeric(10,2),
   ask_1l_quant            numeric(10,2),
   ask_1l_before_quant     numeric(10,2),
   ask_2l_price            numeric(10,2),
   ask_2l_quant            numeric(10,2),
   ask_2l_before_quant     numeric(10,2),
   ask_3l_price            numeric(10,2),
   ask_3l_quant            numeric(10,2),
   ask_3l_before_quant     numeric(10,2)
);
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
   min_ask        numeric(10,2),
   max_bid        numeric(10,2),
   price       numeric(10,2),
   w_ask_1        numeric(10,2),
   l_ask_1        numeric(10,2),
   w_ask_5        numeric(10,2),
   l_ask_5        numeric(10,2),
   w_ask_10       numeric(10,2),
   l_ask_10       numeric(10,2),
   w_ask_20       numeric(10,2),
   l_ask_20       numeric(10,2),
   w_ask_30       numeric(10,2),
   l_ask_30       numeric(10,2),
   w_ask_40       numeric(10,2),
   l_ask_40       numeric(10,2),
   w_ask_50       numeric(10,2),
   l_ask_50       numeric(10,2),
   w_bid_1        numeric(10,2),
   l_bid_1        numeric(10,2),
   w_bid_5        numeric(10,2),
   l_bid_5        numeric(10,2),
   w_bid_10       numeric(10,2),
   l_bid_10       numeric(10,2),
   w_bid_20       numeric(10,2),
   l_bid_20       numeric(10,2),
   w_bid_30       numeric(10,2),
   l_bid_30       numeric(10,2),
   w_bid_40       numeric(10,2),
   l_bid_40       numeric(10,2),
   w_bid_50       numeric(10,2),
   l_bid_50       numeric(10,2)
);


--данные основные по trading view
drop table if exists exmo_info.traiding_view_main;
CREATE TABLE exmo_info.traiding_view_main(
   ID serial primary key,
   par_name          VARCHAR(30),
   check_at       TIMESTAMP ,
   rating            VARCHAR(30),
   prc_change           numeric(20,6),
   abs_change           numeric(20,6),
   high_change          numeric(20,6),
   low_change           numeric(20,6)

);


select * 
from exmo_info.traiding_view_main


--тестовая вставка в traiding_view_main
insert into exmo_info.traiding_view_main (par_name , check_at , rating , prc_change , abs_change , high_change ,low_change)
VALUES ('AEBTC','20170808 1540','sell',1.746725,4.000000e-07,0.000024,0.000022);



--тестовая вставка в тикер
select *
from exmo_info.ticker;

insert into exmo_info.ticker (par_name , check_at , update_at , deal_24h_max , deal_24h_min , deal_24h_avg , deal_last , vol_24h , buy_cur_max , sell_cur_min )
VALUES ('ETH_USD','20170808 1540','20170808 154030' , 1.1 , 1.2 , 1.3 , 1.4 , 1.5 , 1.6 , 1.7);

--тестовая вставка в книгу ордеров
select *
from exmo_info.order_book;


insert into exmo_info.order_book (par_name , check_at , min_ask ,max_bid , price , w_ask_1 , l_ask_1 , w_ask_5 , l_ask_5 , w_ask_10, l_ask_10 , w_ask_20,l_ask_20, w_ask_30, l_ask_30, w_ask_40, l_ask_40, w_ask_50, l_ask_50, w_bid_1, l_bid_1,w_bid_5, l_bid_5, w_bid_10, l_bid_10, w_bid_20, l_bid_20, w_bid_30, l_bid_30, w_bid_40,l_bid_40, w_bid_50, l_bid_50)VALUES ('ETH_USD','20180611 230044',530.99734085,529,529.998670425,530.998781558,2,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,532.9298288,8,528.158880091,3,528.158880091,3,528.158880091,3,525.974009796,17,525.974009796,17,523.723730755,19,523.723730755,19)



--create table and indexes for task
drop table if exists public.user_activity;
CREATE TABLE public.user_activity(
   ID serial primary key,
   user_id           integer,
   event_name           VARCHAR(30),
   event_time     timestamp,
   revenue           numeric(10,2),
   comment VARCHAR(30)
);
CREATE INDEX ON public.user_activity (event_time);

--fill data for test queries
--link to random data spreadsheet https://docs.google.com/spreadsheets/d/1VP5dFqfYA7bCZIakHgqGNlbdZBdgBZKoEQ-wb6ASwrk/edit?usp=sharing
insert into public.user_activity (user_id,event_name,event_time,revenue,comment)
VALUES 
      (1,'install','20190901 010612',0,'new user'),
      (1,'signup','20190902 010612',0,'new user'),
      (1,'payment','20190903 010612',82.2,'new user'),
      (2,'install','20190904 010612',0,'new user'),
      (2,'signup','20190905 010612',0,'new user'),
      (2,'payment','20190906 010612',5.65,'new user'),
      (3,'install','20190907 010612',0,'new user'),
      (3,'signup','20190908 010612',0,'new user'),
      (3,'payment','20190909 010612',25.26,'new user'),
      (4,'install','20190910 010612',0,'new user'),
      (4,'signup','20190911 010612',0,'new user'),
      (4,'payment','20190912 010612',79.86,'new user'),
      (5,'install','20190913 010612',0,'new user'),
      (5,'signup','20190914 010612',0,'new user'),
      (5,'payment','20190915 010612',95.61,'new user'),
      (6,'install','20190916 010612',0,'new user'),
      (6,'signup','20190917 010612',0,'new user'),
      (6,'payment','20190918 010612',51.75,'new user'),
      (7,'install','20190919 010612',0,'new user'),
      (7,'signup','20190920 010612',0,'new user'),
      (7,'payment','20190921 010612',95.93,'new user'),
      (8,'install','20190922 010612',0,'new user'),
      (8,'signup','20190923 010612',0,'new user'),
      (8,'payment','20190924 010612',55.17,'new user'),
      (9,'install','20190925 010612',0,'new user'),
      (9,'signup','20190926 010612',0,'new user'),
      (9,'payment','20190927 010612',57.88,'new user'),
      (10,'install','20190928 010612',0,'new user'),
      (10,'signup','20190929 010612',0,'new user'),
      (10,'payment','20190930 010612',21.22,'new user'),
      (11,'install','20191001 010612',0,'new user'),
      (11,'signup','20191002 010612',0,'new user'),
      (11,'payment','20191003 010612',17.94,'new user'),
      (12,'install','20191004 010612',0,'new user'),
      (12,'signup','20191005 010612',0,'new user'),
      (12,'payment','20191006 010612',5.58,'new user'),
      (13,'install','20191007 010612',0,'new user'),
      (13,'signup','20191008 010612',0,'new user'),
      (13,'payment','20191009 010612',68.83,'new user'),
      (14,'install','20191010 010612',0,'new user'),
      (14,'signup','20191011 010612',0,'new user'),
      (14,'payment','20191012 010612',97.81,'new user'),
      (15,'install','20191013 010612',0,'new user'),
      (15,'signup','20191014 010612',0,'new user'),
      (15,'payment','20191015 010612',4.78,'new user'),
      (16,'install','20191016 010612',0,'new user'),
      (16,'signup','20191017 010612',0,'new user'),
      (16,'payment','20191018 010612',53.71,'new user'),
      (17,'install','20191019 010612',0,'new user'),
      (17,'signup','20191020 010612',0,'new user'),
      (17,'payment','20191021 010612',79.04,'new user'),
      (18,'install','20191022 010612',0,'new user'),
      (18,'signup','20191023 010612',0,'new user'),
      (18,'payment','20191024 010612',89.93,'new user'),
      (19,'install','20191025 010612',0,'new user'),
      (19,'signup','20191026 010612',0,'new user'),
      (19,'payment','20191027 010612',92.29,'new user'),
      (20,'install','20191028 010612',0,'new user'),
      (20,'signup','20191029 010612',0,'new user'),
      (20,'payment','20191030 010612',96.95,'new user'),
      (21,'install','20191031 010612',0,'new user'),
      (21,'signup','20191101 010612',0,'new user'),
      (21,'payment','20191102 010612',63.43,'new user'),
      (22,'install','20191103 010612',0,'new user'),
      (22,'signup','20191104 010612',0,'new user'),
      (22,'payment','20191105 010612',0.85,'new user'),
      (23,'install','20191106 010612',0,'new user'),
      (23,'signup','20191107 010612',0,'new user'),
      (23,'payment','20191108 010612',5.82,'new user'),
      (24,'install','20191109 010612',0,'new user'),
      (24,'signup','20191110 010612',0,'new user'),
      (24,'payment','20191111 010612',19.93,'new user'),
      (25,'install','20191112 010612',0,'new user'),
      (25,'signup','20191113 010612',0,'new user'),
      (25,'payment','20191114 010612',53.81,'new user'),
      (26,'install','20191115 010612',0,'new user'),
      (26,'signup','20191116 010612',0,'new user'),
      (26,'payment','20191117 010612',60.62,'new user'),
      (27,'install','20191118 010612',0,'new user'),
      (27,'signup','20191119 010612',0,'new user'),
      (27,'payment','20191120 010612',90.85,'new user'),
      (28,'install','20191121 010612',0,'new user'),
      (28,'signup','20191122 010612',0,'new user'),
      (28,'payment','20191123 010612',14.41,'new user'),
      (1,'payment','20191020 010612',9.88,'repeat payment in october'),
      (2,'payment','20191020 010612',0.06,'repeat payment in october'),
      (3,'payment','20191020 010612',53.33,'repeat payment in october'),
      (4,'payment','20191020 010612',30.56,'repeat payment in october'),
      (5,'payment','20190912 010612',99.15,'repeat payment in september'),
      (6,'payment','20190912 010612',22.62,'repeat payment in september'),
      (7,'payment','20190912 010612',73.63,'repeat payment in september'),
      (29,'install','20190913 010612',0,'churn before payment'),
      (29,'signup','20190914 010612',0,'churn before payment'),
      (30,'install','20190915 010612',0,'churn before payment'),
      (30,'signup','20190916 010612',0,'churn before payment'),
      (31,'signup','20190917 010612',0,'reg in first pay in second'),
      (31,'install','20190918 010612',0,'reg in first pay in second'),
      (31,'payment','20190928 010612',48.52,'reg in first pay in second')
;


--calc metrics
select sum()
from user_activity



--вот она золотая жила то!!
select par_name
    ,round(deal_last / deal_24h_avg , 3)
    ,deal_last
    ,update_at
from exmo_info.ticker
where par_name = 'ETH_USD'
order by id desc





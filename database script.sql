use pandemic;
drop table city_DB;
drop table infection_deck;
drop table infection_discard;
drop table player_info;


create table city_DB
(
    id varchar(40) not null ,
    city_name varchar(40) default null,
    latitude double default null,
    longitude double default null,
    country_name varchar(40) default null,
    connection varchar(40) default null
);

insert into city_DB
values
    ( 1, 'San Francisco', 37.755228, -122.453053, 'United states'   ,'27 34 2 37'),
    ( 2, 'Chicago'      , 41.856792,  -87.655115, 'United states'   ,'1 5 3 37 38'),
    ( 3, 'Montréal'     , 37.755228, -122.453053, 'United states'   ,'2 4 6'),
    ( 4, 'New York'     , 37.755228, -122.453053, 'United states'   ,'3 6 8 7'),
    ( 5, 'Atlanta'      , 37.755228, -122.453053, 'United states'   ,'2 6 39'),
    ( 6, 'Washington'   , 37.755228, -122.453053, 'United states'   ,'5 3 4 39'),
    ( 7, 'London'       , 37.755228, -122.453053, 'Great Britain'   ,'4 8 9 10'),
    ( 8, 'Madrid'       , 37.755228, -122.453053, 'United states'   ,'42 4 7 9 13'),
    ( 9, 'Paris'        , 37.755228, -122.453053, 'United states'   ,'8 7 10 12 13'),
    (10, 'Essen'        , 37.755228, -122.453053, 'United states'   ,'7 11 12 9'),
    (11, 'St.Petersburg', 37.755228, -122.453053, 'United states'   ,'10 15 16'),
    (12, 'Milan'        , 37.755228, -122.453053, 'United states'   ,'9 10 15'),
    (13, 'Algiers'      , 37.755228, -122.453053, 'United states'   ,'8 9 15'),
    (14, 'Cairo'        , 37.755228, -122.453053, 'United states'   ,'13 15 22 24 46'),
    (15, 'Istanbul'     , 37.755228, -122.453053, 'United states'   ,'13 12 11 16 22 14'),
    (16, 'Moscow'       , 37.755228, -122.453053, 'United states'   ,'15 11 17'),
    (17, 'Tehran'       , 37.755228, -122.453053, 'United states'   ,'16 18 23 22'),
    (18, 'Delhi'        , 37.755228, -122.453053, 'United states'   ,'17 19 20 21 23'),
    (19, 'Kolkata'      , 37.755228, -122.453053, 'United states'   ,'18 20 32 31'),
    (20, 'Chennai'      , 37.755228, -122.453053, 'United states'   ,'21 18 19 32 36'),
    (21, 'MumBai'       , 37.755228, -122.453053, 'United states'   ,'20 18 23'),
    (22, 'Baghdad'      , 37.755228, -122.453053, 'United states'   ,'23 17 15 24 21'),
    (23, 'Karachi'      , 37.755228, -122.453053, 'United states'   ,'24 22 17 18 21'),
    (24, 'Riyadh'       , 37.755228, -122.453053, 'United states'   ,'14 22 23'),
    (25, 'Beijing'      , 37.755228, -122.453053, 'United states'   ,'26 29'),
    (26, 'Seoul'        , 37.755228, -122.453053, 'United states'   ,'25 29 27'),
    (27, 'Tokyo'        , 37.755228, -122.453053, 'United states'   ,'26 29 28 1'),
    (28, 'Osaka'        , 37.755228, -122.453053, 'United states'   ,'27 30'),
    (29, 'Shanghai'     , 37.755228, -122.453053, 'United states'   ,'25 26 27 30 31'),
    (30, 'Taipei'       , 37.755228, -122.453053, 'United states'   ,'29 31 34 28'),
    (31, 'Hong Kong'    , 37.755228, -122.453053, 'United states'   ,'29 30 34 33 32 19'),
    (32, 'Bangkok'      , 37.755228, -122.453053, 'United states'   ,'19 31 33 36 20'),
    (33, 'Ho Chi Minh'  , 37.755228, -122.453053, 'United states'   ,'36 32 31 34'),
    (34, 'Manila'       , 37.755228, -122.453053, 'United states'   ,'33 31 30 36 1'),
    (36, 'Jakarta'      , 37.755228, -122.453053, 'United states'   ,'20 32 33 36'),
    (36, 'Sydney'       , 37.755228, -122.453053, 'United states'   ,'36 34 37'),
    (37, 'Los Angeles'  , 37.755228, -122.453053, 'United states'   ,'36 1 2 38'),
    (38, 'Mexico City'  , 37.755228, -122.453053, 'United states'   ,'37 2 39 40 41'),
    (39, 'Miami'        , 37.755228, -122.453053, 'United states'   ,'38 5 6 40'),
    (40, 'Bogotá'       , 37.755228, -122.453053, 'United states'   ,'38 39 42 43 41'),
    (41, 'Lima'         , 37.755228, -122.453053, 'United states'   ,'44 38 40 '),
    (42, 'São Paulo'    , 37.755228, -122.453053, 'United states'   ,'43 40 8 45'),
    (43, 'Buenos Rires' , 37.755228, -122.453053, 'United states'   ,'40 42'),
    (44, 'Santiago'     , 37.755228, -122.453053, 'United states'   ,'41'),
    (45, 'Lagos'        , 37.755228, -122.453053, 'United states'   ,'42 46 48'),
    (46, 'Khartoum'     , 37.755228, -122.453053, 'United states'   ,'45 48 47 14'),
    (47, 'Johannesburg' , 37.755228, -122.453053, 'United states'   ,'48 46'),
    (48, 'Kinshasa'     , 37.755228, -122.453053, 'United states'   ,'45 46 47');

create table player_info
(
    player_id varchar(40) not null ,
    player_name varchar(40) default null,
    city_id varchar(40)  not null
);

create table infection_deck
(
    city_id varchar(40) default null
);

create table infection_discard
(
    city_id varchar(40) default null
);

insert into player_info
values
    (1,'thinh',2),
    (2,'Lu',3);


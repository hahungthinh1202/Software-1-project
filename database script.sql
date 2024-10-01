use pandemic;
drop table city_DB;
drop table city_current;
drop table infection_deck;;
drop table infection_discard;
drop table player_current;
drop table player_own;
drop table game_current;
drop table player_card_current;


create table city_DB
(
    id varchar(40) not null ,
    city_name varchar(40) default null,
    latitude double default null,
    longitude double default null,
    country_name varchar(40) default null,
    virus varchar(40) default null,
    connection varchar(40) default null
);

create table city_current
(
    city_id varchar(40) not null ,
    red int default 0,
    blue int default 0,
    yellow int default 0,
    black int default 0,
    research_center bool default false,
    is_outbreak bool default false
);

insert into city_DB
values
    ( 1, 'San Francisco', 103, 252, 'United states'   ,'blue','27 34 2 37'),
    ( 2, 'Chicago'      , 212, 220, 'United states'   ,'blue','1 5 3 37 38'),
    ( 3, 'Montréal'     , 279, 197, 'Canada'          ,'blue','2 4 6'),
    ( 4, 'New York'     , 356, 188, 'United states'   ,'blue','3 6 8 7'),
    ( 5, 'Atlanta'      , 221, 267, 'United states'   ,'blue','2 6 39'),
    ( 6, 'Washington'   , 330, 266, 'United states'   ,'blue','5 3 4 39'),
    ( 7, 'London'       , 37.755228, -122.453053, 'United Kingdom'  ,'blue','4 8 9 10'),
    ( 8, 'Madrid'       , 37.755228, -122.453053, 'Spain'           ,'blue','42 4 7 9 13'),
    ( 9, 'Paris'        , 37.755228, -122.453053, 'France'          ,'blue','8 7 10 12 13'),
    (10, 'Essen'        , 37.755228, -122.453053, 'Germany'         ,'blue','7 11 12 9'),
    (11, 'St.Petersburg', 37.755228, -122.453053, 'Russia'          ,'blue','10 15 16'),
    (12, 'Milan'        , 37.755228, -122.453053, 'Italy'           ,'blue','9 10 15'),
    (13, 'Algiers'      , 37.755228, -122.453053, 'Algeria'         ,'black','8 9 15'),
    (14, 'Cairo'        , 37.755228, -122.453053, 'Egypt'           ,'black','13 15 22 24 46'),
    (15, 'Istanbul'     , 37.755228, -122.453053, 'Turkey'          ,'black','13 12 11 16 22 14'),
    (16, 'Moscow'       , 37.755228, -122.453053, 'Russia'          ,'black','15 11 17'),
    (17, 'Tehran'       , 37.755228, -122.453053, 'Iran'            ,'black','16 18 23 22'),
    (18, 'Delhi'        , 37.755228, -122.453053, 'India'           ,'black','17 19 20 21 23'),
    (19, 'Kolkata'      , 37.755228, -122.453053, 'India'           ,'black','18 20 32 31'),
    (20, 'Chennai'      , 37.755228, -122.453053, 'India'           ,'black','21 18 19 32 36'),
    (21, 'MumBai'       , 37.755228, -122.453053, 'India'           ,'black','20 18 23'),
    (22, 'Baghdad'      , 37.755228, -122.453053, 'Iraq'            ,'black','23 17 15 24 21'),
    (23, 'Karachi'      , 37.755228, -122.453053, 'Pakistan'        ,'black','24 22 17 18 21'),
    (24, 'Riyadh'       , 37.755228, -122.453053, 'Saudi Arabia'    ,'black','14 22 23'),
    (25, 'Beijing'      , 37.755228, -122.453053, 'China'           ,'red','26 29'),
    (26, 'Seoul'        , 37.755228, -122.453053, 'South Korea'     ,'red','25 29 27'),
    (27, 'Tokyo'        , 37.755228, -122.453053, 'Japan'           ,'red','26 29 28 1'),
    (28, 'Osaka'        , 37.755228, -122.453053, 'Japan'           ,'red','27 30'),
    (29, 'Shanghai'     , 37.755228, -122.453053, 'China'           ,'red','25 26 27 30 31'),
    (30, 'Taipei'       , 37.755228, -122.453053, 'Taiwan'          ,'red','29 31 34 28'),
    (31, 'Hong Kong'    , 37.755228, -122.453053, 'Hong Kong'       ,'red','29 30 34 33 32 19'),
    (32, 'Bangkok'      , 37.755228, -122.453053, 'Thailand'        ,'red','19 31 33 36 20'),
    (33, 'Ho Chi Minh'  , 37.755228, -122.453053, 'Vietnam'         ,'red','36 32 31 34'),
    (34, 'Manila'       , 37.755228, -122.453053, 'Philippines'     ,'red','33 31 30 36 1'),
    (36, 'Jakarta'      , 37.755228, -122.453053, 'Indonesia'       ,'red','20 32 33 36'),
    (36, 'Sydney'       , 37.755228, -122.453053, 'Australia'       ,'red','36 34 37'),
    (37, 'Los Angeles'  , 37.755228, -122.453053, 'United states'   ,'yellow','36 1 2 38'),
    (38, 'Mexico City'  , 37.755228, -122.453053, 'Mexico'          ,'yellow','37 2 39 40 41'),
    (39, 'Miami'        , 37.755228, -122.453053, 'United states'   ,'yellow','38 5 6 40'),
    (40, 'Bogotá'       , 37.755228, -122.453053, 'Colombia'        ,'yellow','38 39 42 43 41'),
    (41, 'Lima'         , 37.755228, -122.453053, 'Peru'            ,'yellow','44 38 40 '),
    (42, 'São Paulo'    , 37.755228, -122.453053, 'Brazil'          ,'yellow','43 40 8 45'),
    (43, 'Buenos Aires' , 37.755228, -122.453053, 'Argentina'       ,'yellow','40 42'),
    (44, 'Santiago'     , 37.755228, -122.453053, 'Chile'           ,'yellow','41'),
    (45, 'Lagos'        , 37.755228, -122.453053, 'Nigeria'         ,'yellow','42 46 48'),
    (46, 'Khartoum'     , 37.755228, -122.453053, 'Sudan'           ,'yellow','45 48 47 14'),
    (47, 'Johannesburg' , 37.755228, -122.453053, 'South Africa'    ,'yellow','48 46'),
    (48, 'Kinshasa'     , 37.755228, -122.453053, 'Congo'           ,'yellow','45 46 47');

create table player_current
(
    player_id varchar(40) not null ,
    player_name varchar(40) default null,
    city_id varchar(40)  not null,
    role varchar(40) default null,
    game_id varchar(40) not null
);

create table infection_deck
(
    city_id varchar(40) default null
);

create table infection_discard
(
    city_id varchar(40) default null
);

insert into player_current
values
    (1,'thinh',5,'medic','g1'),
    (2,'Lu',5,'scientist','g1');


create table player_own
(

    player_id varchar(40) not null,
    card_id varchar(40) not null
);

create table player_card_current
(
    id varchar(40) not null,
    city_id varchar(40) default null
);

create table game_current
(
    game_id varchar(40) not null,
    infection_track int default 0,
    outbreak_track int default 0,
    current_player_card int default 1
);

insert into game_current
values ('g1',0,0, 1);

select player_card_current.city_id from player_card_current
where player_card_current.id = 12




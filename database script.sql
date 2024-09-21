create table infection_card
(
    id int not null ,
    city_name varchar(40) default null,
    latitude double default null,
    longitude double default null,
    primary key (id)
);
DROP KEYSPACE IF EXISTS mainkeyspace;

CREATE KEYSPACE mainkeyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE mainkeyspace;

CREATE TABLE Movies(
    id bigint PRIMARY KEY, 
    popularity float, 
    title text, 
    release_date date, 
    vote_average float, 
    vote_count int, 
    genres text
);


CREATE TABLE TVs(
    id bigint PRIMARY KEY, 
    origin_country text, 
    popularity float, 
    name text, 
    first_air_date date, 
    vote_average float, 
    vote_count int,
    genres text
);
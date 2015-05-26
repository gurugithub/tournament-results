-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.






-- Creating table for storing tournaments so that database is useable across tournaments

drop table tournament_name cascade;
create table tournament_name ( tid integer primary key not null, tname varchar(80) not null, tdate date default CURRENT_DATE);

-- test --
insert into tournament_name values (1,'Udacity',DEFAULT);
-- create table for players

drop table players cascade;
create table players (playerid SERIAL primary key not null, playername varchar(80) not null, country varchar(3) default 'US', wins integer default 0);

-- test players--

-- insert into players values (DEFAULT,'Lewis Hamilton',DEFAULT);
-- insert into players values (DEFAULT,'Fernando Alonso',DEFAULT);

-- create matcches--

drop table matches;
drop type result;
CREATE TYPE result AS ENUM ('won', 'lost', 'tied');
create table matches ( matchid SERIAL primary key not null, tid integer references tournament_name(tid), playerid integer references players(playerid), standings result  , tdate date default CURRENT_DATE);



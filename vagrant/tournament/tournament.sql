-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


--Create tournament database
create database tournament;


--Create table to log matches played.
create table matches (match_id serial, player_1 integer, player_2 integer, winner integer);
--   Column  |  Type   |                         Modifiers                          
-- ----------+---------+------------------------------------------------------------
--  match_id | integer | not null default nextval('matches_match_id_seq'::regclass)
--  player_1 | integer | 
--  player_2 | integer | 
--  winner   | integer | 


--Create table of players registered
create table players (player_id serial, player_name text);
--       Column       |  Type   |                          Modifiers                          
-- -------------------+---------+-------------------------------------------------------------
--  player_id         | integer | not null default nextval('players_player_id_seq'::regclass)
--  player_name       | text    | 


--Create view for total matches.
create view total_matches as 
select p.player_id as player, case when count(subq.player_1) = null then 0 else count(*) end as total_matches 
from players p left join (select player_1 from matches union all select player_2 from matches) 
as subq
on  p.player_id = subq.player_1
group by p.player_id, subq.player_1 
order by player;


--Better way to display total_matches so that it returns 0's rather than blanks when games have not yet been played.
create view total_matches_1 as 
 select p.player_id as player, count (tm.total_matches)
 from players p left join total_matches tm
 on p.player_id = tm.player
 group by p.player_id;


--Create view for aggregated wins.
create view wins as 
	select t1.player, t1.name, t1.num_of_wins 
	from (select p.player_id as player, p.player_name as name, count(m.winner) as num_of_wins 
		from players p left join matches m 
		on p.player_id = m.winner 
		group by p.player_id, p.player_name) as t1;


--Show standings including wins and total matches played.
 create view standings as
 select w.player, w.name, w.wins, tm.count as total_matches 
 from wins w left join total_matches_1 tm on w.player = tm.player 
 group by w.player, w.name, w.wins, tm.count 
 order by wins desc;





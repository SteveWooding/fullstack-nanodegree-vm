-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Delete any old tournament database that might be hanging around
DROP DATABASE IF EXISTS tournament;

-- Create the tournament database
CREATE DATABASE tournament;

-- Connect to the tournament database
\c tournament;

-- Table containing the registered players, id and name.
CREATE TABLE players ( id serial PRIMARY KEY,
                       name text);

-- Table of matchers played, each row having the winner and loser ids.
CREATE TABLE matches ( winner_pid int references players(id),
                       loser_pid int references players(id));

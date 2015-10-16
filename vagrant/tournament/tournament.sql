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
                       name text,
                       had_bye boolean);

-- Table of matchers played, each row having the winner and loser ids.
CREATE TABLE matches ( winner_pid int references players(id),
                       loser_pid int references players(id));

-- View of the number of wins each player has achieved.
-- Columns: Player ID, Number of Wins
CREATE VIEW num_wins
    AS SELECT players.id, count(matches.winner_pid) AS wins
    FROM players left join matches
    ON players.id = matches.winner_pid
    GROUP BY players.id;

-- View of number of matches each player has played.
-- Columns: Player ID, Number of Matches Played
CREATE VIEW num_matches
    AS SELECT players.id, count(combine) AS num_matches
    FROM players left join
        (SELECT winner_pid AS combine FROM matches UNION ALL SELECT loser_pid FROM matches) AS combine
    ON players.id = combine
    GROUP BY players.id;

-- View of number of wins and matches for each player.
-- Columns: Player ID, Number of Wins, Number of Matches
CREATE VIEW num_matches_wins
    AS SELECT num_matches.id, num_wins.wins, num_matches.num_matches AS matches
    FROM num_matches, num_wins
    WHERE num_matches.id = num_wins.id;
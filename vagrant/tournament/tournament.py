#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import shuffle


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("DELETE FROM matches;")
    tour_db.commit()
    tour_db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("DELETE FROM players;")
    tour_db.commit()
    tour_db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("SELECT COUNT(*) FROM players;")
    count = cur.fetchone()[0]
    tour_db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    tour_db.commit()
    tour_db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    tour_db = connect()
    cur = tour_db.cursor()
    query = ("SELECT num_matches_wins.id, players.name, num_matches_wins.wins, "
             "       num_matches_wins.matches "
             "FROM players, num_matches_wins "
             "WHERE players.id = num_matches_wins.id "
             "ORDER BY num_matches_wins.wins desc;")
    cur.execute(query)
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3])) for row in cur.fetchall()]
    tour_db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("INSERT INTO matches (winner_pid, loser_pid) VALUES (%s, %s);", (winner, loser))
    tour_db.commit()
    tour_db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Get a count of the number of matches played.
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("SELECT COUNT(*) FROM matches;")
    total_num_matches = cur.fetchone()[0]
    tour_db.close()

    # Get the current player standings
    standings = playerStandings()

    # If number of matches is zero, then need a random pairing for the 1st round
    if total_num_matches == 0:
        # Randomly shuffle the standings in place.
        shuffle(standings)

    # Otherwise pair up according to the number of wins.
    # The standings are ordered by number of wins so just go down the list,
    # two at a time.
    pairings = []
    standings_it = iter(standings)
    for home_player in standings_it:
        away_player = next(standings_it)
        pairings.append((home_player[0], home_player[1], away_player[0], away_player[1]))

    return pairings

    # Credits
    # Idea for using an iterator to go through a list two items at a time was found
    # on this Stack Overflow page: http://stackoverflow.com/questions/16789776/
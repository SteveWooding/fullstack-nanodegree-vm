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

def check_for_rematch(player_id1, player_id2):
    """Checks whether the two players specificed have played a match before.

    Args:
      player_id1: ID of first player
      player_id2: ID of second player

    Returns:
      Bool: True if they have met before, False if they have not.
    """
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("""SELECT EXISTS(SELECT 1
                                 FROM matches
                                 WHERE winner_pid=%(id1)s AND loser_pid=%(id2)s
                                   OR   winner_pid=%(id2)s AND loser_pid=%(id1)s);""",
                {'id1': player_id1, 'id2': player_id2})
    is_rematch = cur.fetchone()[0]
    tour_db.close()

    return is_rematch

    # Credits
    # Idea for using the EXISTS PSQL keyword found on this Stack Overflow page:
    # http://stackoverflow.com/questions/7471625/


def id_to_name(player_id):
    """Returns a player's name based on a given ID number.

    Args:
      player_id: ID of player

    Returns:
      Str: Player's name.
    """
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("SELECT name FROM players WHERE id=%s", (player_id,))
    player_name = cur.fetchone()[0]
    tour_db.close()

    return player_name


def all_pairs(lst):
    """Takes a list and generates all the unique pairs it contains.

    The order of the pairs is not important and the ordering of each pair is not important.
    The list must be of even length.

    This function was written by gatoatigrado (Stack Overflow username) and the orginal can
    be found here: http://stackoverflow.com/a/13020502

    I have used this function as it precisely gives me what I wanted, without producing
    excessive repeated pairings for this application.

    Args:
        lst (list): a list of items to be paired up

    Yields:
        list: The next set of pairs. Each pair consists of items from the orginal list placed
            within a tuple.

    Example:
        Here is an example of the output for a list of 4 items.

        >>> for pairs in all_pairs([1, 2, 3, 4]):
                print pairs
        [(1, 2), (3, 4)]
        [(1, 3), (2, 4)]
        [(1, 4), (2, 3)]

        For a list of 4 items, the argument to the itertools.product() function is:
            [0, 1, 2], [0]

        Which will produce the following output from the product() function:
            (0, 0)
            (1, 0)
            (2, 0)

        So these results mean there will be 3 sets of pairs containing 2 pairs each.

        For the first set (0, 0), the pop function is always pop(0) - taking the first
        item off the temp list. So this just produces two pairs in the same order as per
        the original list.

        For set (1, 0), the first pair is (1, 3), as the first item of the first pair is
        always the first item from the original list and the 1 means an item is skipped
        and 3 is selected. The second pair is just what is left, (2, 4).

        For set (2, 0), 2 items are skipped, so the first pair is (1, 4). Then what's left is
        (2, 3) for the 2nd pair.

    """
    # Check to make sure there are an even number of items in the list.
    list_length = len(lst)
    if list_length % 2 != 0:
        raise ValueError("The list must have an even number of items.")

    # Create an iterater that goes through all the choices of which item to pair up next.
    choice_indices = itertools.product(*[xrange(k) for k in reversed(xrange(1, list_length, 2))])

    # Generate a list of pairs for each choice
    for choice in choice_indices:
        # Create a temporary copy of the list, so it can be consumed by calls to pop().
        tmp = lst[:]
        result = []

        # Go through this choice of indices, consuming the temp list two items at a time
        # creating pairs and creating the set of pairs in result.
        for index in choice:
            result.append((tmp.pop(0), tmp.pop(index)))

        yield result


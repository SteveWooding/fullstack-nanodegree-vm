#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools
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


def reportMatch(winner, loser=None):
    """Records the outcome of a single match between two players.
    
    If only one player ID is given, this indicates that a bye is to be given to
    that player. A null is recorded in the loser_pid column of the matches table.

    Args:
        winner (int):  the id number of the player who won
        loser (int) [optional]:  the id number of the player who lost
    """
    tour_db = connect()
    cur = tour_db.cursor()
    
    if loser is None:
        # So a bye is to be given to player `winner`.
        # Check to see whether player `winner` has be give a bye before.
        cur.execute("SELECT had_bye FROM players WHERE id=%s", (winner,))
        had_bye = cur.fetchone()[0]
        
        if had_bye is True:
            print "Error: Player has already had a bye."
            tour_db.close()
            return
        
        # Update the had_bye attribute of the player.
        cur.execute("UPDATE players SET had_bye=TRUE WHERE id=%s", (winner,))
    
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
    # Declare a list object to store the pairings.
    pairings = []

    # Get a count of the number of matches played.
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("SELECT COUNT(*) FROM matches;")
    total_num_matches = cur.fetchone()[0]

    # Get the current player standings
    standings = playerStandings()

    # Check to see if there are an odd number of players.
    have_odd_players = False
    if len(standings) % 2 != 0:
        have_odd_players = True

    # If number of matches is zero, then need a random pairing for the 1st round
    if total_num_matches == 0:
        # Randomly shuffle the standings in place.
        shuffle(standings)

        # If we have an odd number of players, we need to deal with a bye for a player.
        # Let's keep track of that.
        if have_odd_players is True:
            dealt_with_bye = False

        # Go through standings two at a time and generate the pairings [1].
        standings_it = iter(standings)
        for home_player in standings_it:
            if have_odd_players is True and dealt_with_bye is False:
                pairings.append((home_player[0], home_player[1], home_player[0], 'Give a Bye'))
                dealt_with_bye = True
            else:
                away_player = next(standings_it)
                pairings.append((home_player[0], home_player[1], away_player[0], away_player[1]))

        tour_db.close()
        return pairings

    # Check to see if all players have played the same number of matches.
    cur.execute("SELECT MAX(num_matches) FROM num_matches;")
    max_num_matches = cur.fetchone()[0]
    cur.execute("SELECT MIN(num_matches) FROM num_matches;")
    min_num_matches = cur.fetchone()[0]

    if max_num_matches != min_num_matches:
        tour_db.close()
        print "Incomplete previous round. Please report more matches."
        return None

    # Compile a list of win groupings
    max_num_wins = standings[0][2]
    win_groups = []
    for wins in xrange(0, max_num_wins + 1):
        cur.execute("SELECT id FROM num_wins WHERE wins=%s", (wins,))
        res = [int(row[0]) for row in cur.fetchall()]
        win_groups.append(res)

    # Finished with the database in this function, so let's be nice and close it.
    tour_db.close()

    # If only 1 player in the top win group, then we have an overall winner, so
    # no need to have another round of pairings.
    if len(win_groups[-1:][0]) == 1:
        print "An overall winner already exists. No further round required."
        return None

    # Deal with giving a player a bye.
    if have_odd_players is True:
        # Get a player that hasn't alreay taken a bye.
        bye_player_id = select_player_for_bye()

        # Remove this player from the win groups.
        for win_group in win_groups:
            if win_group.count(bye_player_id) > 0:
                win_group.remove(bye_player_id)
                break

        # Add this bye match to the pairings.
        bye_player_name = id_to_name(bye_player_id)
        pairings.append((bye_player_id, bye_player_name, bye_player_id, 'Give a Bye'))

    # Check to see if any of the win groups contains an odd number of players.
    for i in xrange(0, len(win_groups)):
        if len(win_groups[i]) % 2 != 0:
            move_item_to_list(win_groups, i)

    # Generate pairings until no rematches exist in the pairings
    pairing_success = False
    while pairing_success is False:
        pairings_res, error_in_group = generate_pairings(win_groups)
        if error_in_group is None:
            # Found valid pairings, so exist the while loop.
            pairing_success = True

        else:
            # Could not find non-repeated matches in a win group.
            if error_in_group + 2 > len(win_groups):
                print "Error: Can't find a set of pairings with no repeats."
                return None

            # Add two players from the next group to the erroring group.
            move_item_to_list(win_groups, error_in_group)
            move_item_to_list(win_groups, error_in_group)

        # Go around the loop again and try to generate valid pairings

    # Add the pairings result from generate_pairings() to pairings.
    pairings.extend(pairings_res)

    return pairings

    # Credits
    # [1] Idea for using an iterator to go through a list two items at a time was found
    # on this Stack Overflow page: http://stackoverflow.com/questions/16789776/


def check_for_rematch(player_id1, player_id2):
    """Checks whether the two players specified have played a match before.

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


def generate_pairings(win_groups):
    """Generates pairings given player IDs sorted into win groups.

    Args:
        win_groups (list): A list where each item is a list of player ids with the same
            number of wins (though this may be adjusted if no non-repeated match ups could
            found previously).

    Returns:
        pairings (list): A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name

        idx (int): If no non-repeated match ups could be found, this tells the calling
            function which win group the issue is in so it can be resolved.
    """
    # For each win group, try each combination of matches, checking for rematches.
    pairings = []
    for idx, win_group in enumerate(win_groups):
        win_group_success = False
        # Go through each pair in the win group, checking for rematches.
        for pairs in all_pairs(win_group):
            # Go through each pair in the win group, checking for rematches.
            contains_rematch = False
            for pair in pairs:
                is_rematch = check_for_rematch(pair[0], pair[1])
                if is_rematch is True:
                    contains_rematch = True
                    break

            if contains_rematch is True:
                # This set of pairs contains a rematch. Try the next pairing permutation.
                continue
            else:
                win_group_success = True
                for pair in pairs:
                    # Add this pairing to the pairings
                    player1_name = id_to_name(pair[0])
                    player2_name = id_to_name(pair[1])
                    pairings.append((pair[0], player1_name, pair[1], player2_name))
                break

        # If there was no success on any pair permutation, return to swissPairings()
        # to adjust the groupings.
        if win_group_success is False:
            return None, idx

    return pairings, None


def all_pairs(lst):
    """Takes a list and generates all the unique pairs it contains.

    The order of the pairs is not important and the ordering of each pair is not important.
    The list must be of even length.

    This function was written by gatoatigrado (Stack Overflow username) and the original can
    be found here: http://stackoverflow.com/a/13020502

    I have used this function as it precisely gives me what I wanted, without producing
    excessive repeated pairings for this application.

    Args:
        lst (list): a list of items to be paired up

    Yields:
        list: The next set of pairs. Each pair consists of items from the original list placed
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

    # Create an iterator that goes through all the choices of which item to pair up next.
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


def move_item_to_list(list_of_lists, target_list_idx):
    """Takes a list of lists and moves one item to the list specified from the next list.

    This function works in-place upon the list of lists.

    Args:
        list_of_lists (list): A list of lists.
        target_list_idx (int): Index of the list that will have an item moved to it.

    Returns:
        None: The list is modified in place.
    """
    # Check to see if the next list exists
    if target_list_idx + 2 > len(list_of_lists):
        raise IndexError("No list to move an item from exists.")

    # Add an element from the next group to the group specified in the arguments
    list_of_lists[target_list_idx].append(list_of_lists[target_list_idx + 1].pop(0))

    # Check to see if the above operation created an empty group. If so then remove it.
    if len(list_of_lists[target_list_idx + 1]) == 0:
        del list_of_lists[target_list_idx + 1]

    return None


def select_player_for_bye():
    """Returns a player id of a player that hasn't already taken a bye.

    The query to the database makes sure to return the player with the fewest number
    of wins, to avoid a situation where one of the top players wins the tournament
    with a bye.

    Returns:
        non_bye_player_id (int): The player id of a player that hasn't taken a bye.
    """
    tour_db = connect()
    cur = tour_db.cursor()
    cur.execute("""SELECT players.id
                   FROM players, num_wins
                   WHERE players.had_bye=FALSE and players.id = num_wins.id
                   ORDER BY num_wins.wins;""")
    non_bye_player_id = cur.fetchone()[0]
    tour_db.close()

    return non_bye_player_id

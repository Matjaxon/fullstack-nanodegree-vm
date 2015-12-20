#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()  #establish connection to db.
    c = conn.cursor()  #create cursor
    c.execute ("delete from matches")  #execute psql query/action
    conn.commit()  #commit changes
    conn.close()  #close connection

def deletePlayers():
     """Remove all the player records from the database."""
     conn = connect()
     c = conn.cursor()
     c.execute("delete from players")
     conn.commit()
     conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) as num from players")
    results = c.fetchall()
    return results[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (player_name) values (%s)", (name,)) #inserting name as a tuple.
    conn.commit()
    conn.close()	 


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
    conn = connect()
    c = conn.cursor()
    query = """select * from standings"""
    c.execute(query)
    results = c.fetchall()  #retrieve results from postgresql results table.
    return results  #return results for next function to use.
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner_string = str(winner)
    loser_string = str(loser)
    conn = connect()
    c = conn.cursor()
    query = "insert into matches (player_1, player_2, winner) values ({0}, {1}, {2})".format(winner_string, loser_string, winner_string)
    c.execute(query)
    conn.commit()
    conn.close()


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
    conn = connect()
    c = conn.cursor()
    get_ids_query = "select player, name from standings"
    c.execute(get_ids_query)
    rankings = c.fetchall()
    num_of_matches = len(rankings)/2
    match = 0  #match will be increased by 1 after each pair of players is combined into a list item.
    player_position = 0  #player_positin will be increased by 1 after each player id and name is utilized.
    pairings = []  #empty list for the Swiss pairings to be appended to
    while match < 2:
    	pairing = (rankings[player_position][0], rankings[player_position][1],)  #grab first player of a pairing
    	player_position += 1
    	pairing = pairing + (rankings[player_position][0], rankings[player_position][1],)  #grab second player of a pairing
    	pairings.append(pairing)  #append individual pairing to the pairings list
    	player_position += 1
    	match += 1
    return pairings


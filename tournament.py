#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute( "delete from matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute( "delete from players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect() 
    cursor = DB.cursor()
    cursor.execute( "select count(*) as num from players")
    row = cursor.fetchone()
    
    DB.close()
    # posts.sort(key=lambda row: row['time'], reverse=True)
    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect() 
    cursor = DB.cursor()
    cursor.execute( "INSERT INTO players (playername) values (%s)", (bleach.clean(name),))
    DB.commit()
    DB.close()
    


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
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(" select players.playerid, players.playername, sum(players.wins) as wins, count(matches.playerid) as played from players left outer join  matches on players.playerid = matches.playerid  group by players.playerid order by wins ;")
    
    rows = cursor.fetchall()
#    for i, row in enumerate(rows):
#       print "Row", i, "value = ", row[0]
    
    DB.close()
    
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    DB = connect() 
    cursor = DB.cursor()
    cursor.execute( "INSERT INTO matches (tid, playerid, standings) values (1, %s, 'won')", (bleach.clean(winner), ))
    cursor.execute( "INSERT INTO matches (tid, playerid, standings) values (1, %s, 'lost')", (bleach.clean(loser), ))
    cursor.execute( "update players SET wins = wins + 1 where playerid = (%s) ", (winner,))
    DB.commit()
    DB.close()
    
 
 
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

    DB = connect()
    cursor = DB.cursor()
    cursor.execute(" select playerid, playername from players order by wins desc")
    
    results = []
    
    rows = cursor.fetchall()
    id1 = 0
    name1 = ""
    id2 = 0
    name2 = ""
    
    for i, row in enumerate(rows):
        
        
        if (i % 2) == 0:
            id1 = (row[0])
            name1 = (row[1])
#            print "Not equal"
        
        if (i % 2) != 0:
            id2 = (row[0])
            name2 = (row[1])
            result = id1, name1, id2, name2
#            print "equal"
            results.append(result)
                      
    DB.close()

    
    return results

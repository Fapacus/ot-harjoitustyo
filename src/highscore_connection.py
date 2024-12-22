import sqlite3

def highscore_connection(scoreboard="scoreboard.db"):
    score_connection = sqlite3.connect(scoreboard)
    return score_connection

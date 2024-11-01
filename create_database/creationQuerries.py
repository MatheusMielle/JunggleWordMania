
"""
Game code would be defined when player clicks to start a game
TODO: A way to differentiate Single player to classroom
IDEA: Classroom codes would start with the char C while single players with S
"""


def createPlayer():
    sql =  "CREATE TABLE PLAYER ("
    sql += "Player_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    sql += "Player_name VARCHAR(50) NOT NULL,"
    sql += "Game_code VARCHAR(8) NOT NULL,"
    sql += "Time VARCHAR(20),"
    sql += "FOREIGN KEY (Game_code) REFERENCES GAME(Game_code) ON DELETE CASCADE"
    sql += ");"
    return sql

def createGame():
    sql =  "CREATE TABLE GAME ("
    sql += "Game_code VARCHAR(8) NOT NULL PRIMARY KEY,"
    sql += "Is_classroom BOOLEAN NOT NULL"
    sql += ");"
    return sql

def createWord():
    sql =  "CREATE TABLE WORD ("
    sql += "Word_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    sql += "Word VARCHAR(255) NOT NULL,"
    sql += "Definition TEXT NOT NULL,"
    sql += "Difficulty VARCHAR(20)"
    sql += ");"
    return sql

def createGameWords():
    sql =  "CREATE TABLE GAME_WORDS ("
    sql += "Game_code VARCHAR(8) NOT NULL,"
    sql += "Word_ID INT NOT NULL,"
    sql += "PRIMARY KEY (Game_code, Word_ID),"
    sql += "FOREIGN KEY (Game_code) REFERENCES GAME(Game_code) ON DELETE CASCADE,"
    sql += "FOREIGN KEY (Word_ID) REFERENCES WORD(Word_ID) ON DELETE CASCADE"
    sql += ");"
    return sql

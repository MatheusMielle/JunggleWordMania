import random
import string
import json
import pymysql
from fileInputValidator import validate

# Load the JSON data from the file
secrets = open('data/secrets.json', 'r')
data = json.load(secrets)


#Start a connection
db = pymysql.connect(host=data['mysql']['host'], user=data['mysql']['user'], password=data['mysql']['password'])

#Create the database cursor
c = db.cursor()

c.execute("USE ScrambleGame;")

def generate_game_code(is_classroom):
    """
    Generate a unique game code.

    The game code is prefixed with 'C' for classroom games and 'S' for single player games,
    followed by 7 random alphanumeric characters. The function ensures that the generated
    game code does not already exist in the database.

    Args:
        is_classroom (bool): Indicates whether the game is for a classroom (True) or standard (False).

    Returns:
        str: A unique game code prefixed with 'C' or 'S'.

    Raises:
        Exception: If there is an error while accessing the database.
    """

    # Define the characters to use for the game code
    characters = string.ascii_uppercase + string.digits
    
    # prefix the game_code with C or S depending on the game type
    letter = "C" if is_classroom else "S"

    # keeps generating game codes until a unique one is found
    while True:
        # gamecode is 8 characters long
        # the first character is either C or S depending on the game type
        # the remaining 7 characters are random letters and digits
        game_code = letter + ''.join(random.choice(characters) for _ in range(7))
        if game_code not in get_game_codes():  # Check against all existing codes
            break

    print("generated game code:" + game_code)

    return game_code


def save_game_code(game_code, is_classroom):
    """
    Save the generated game code to the database.

    This function inserts a new game code into the game table in the database.
    The function assumes that 'Is_classroom' is set to True for all saved game codes.

    Args:
        game_code (str): The game code to be saved in the database.
        is_classroom (bool): Indicates whether the game is for a classroom (True) or standard (False).

    Returns:
        None

    Raises:
        pymysql.MySQLError: If there is an error while executing the SQL command.
    """
    c.execute(f"INSERT INTO game(game_code, Is_classroom) VALUES ('{game_code}', {is_classroom});")
    db.commit()

#Future work: there is a faster way to do this in SQL. 
#Saving all codes in a list and checking may slow us down if lots of data
def get_game_codes():
    """
    Retrieve all existing game codes from the database.

    This function queries the database and returns a list of all game codes currently stored
    in the game table.

    Returns:
        list: A list of strings representing the existing game codes.

    Raises:
        pymysql.MySQLError: If there is an error while executing the SQL command.
    """
    c.execute("SELECT game_code FROM game")
    return [row[0] for row in c.fetchall()] 



def save_player(username, code):
    """
    Save player information in the database and return the player's ID.

    This function inserts the username and associated game code into the PLAYER table,
    and returns the auto-incremented player ID.

    Args:
        username (str): The player's username to be inserted.
        code (str): The game code associated with the player.

    Returns:
        int: The auto-incremented player ID.

    Raises:
        pymysql.MySQLError: If there is an error while executing the SQL command.
    """

    c.execute(f"INSERT INTO PLAYER(Player_name, Game_code) VALUES ('{username}', '{code}');")
    db.commit()
    return c.lastrowid



def create_game(game_code, nWords=None, difficulty=None, file=None):
    """
    Create a game and insert words into the game.

    This function creates a new game by inserting selected words into the `game_words` table.
    The function can either randomly select words based on difficulty or use words provided 
    through a file.

    Args:
        game_code (str): The unique code for the game.
        nWords (int, optional): The number of words to select for the game if not using a file.
        difficulty (str, optional): The difficulty level of the words to be selected.
        file (File, optional): A file containing words and definitions in the format `WORD, DEFINITION`.

    Raises:
        pymysql.MySQLError: If there is an error while executing the SQL command.
    """

    if file is None:
        # Retrieve word IDs based on the specified difficulty
        c.execute(f"SELECT Word_ID FROM word WHERE Difficulty = '{difficulty}';")
        wordIds = [row[0] for row in c.fetchall()]

        # Randomly select nWords from the retrieved word IDs
        wordIds = random.sample(wordIds, int(nWords))

        # Insert selected word IDs into game_words table
        for elm in wordIds:
            c.execute(f"INSERT INTO game_words(Game_code, Word_ID) VALUES ('{game_code}', '{elm}');")
    else:
        words = []

        # Read words and definitions from the specified file
        for line in file:
            line = line.decode('utf-8').strip()
            line = line.replace("'", "''") 
            word, definition = line.split(',', 1)
            words.append([word, definition])

            # Insert the word and its definition into the Word table
            c.execute(f"INSERT INTO Word(Word, Definition) VALUES ('{word}','{definition}')")

        db.commit()  # Commit changes after inserting all words

        # Retrieve the IDs of the inserted words and add them to game_words
        for w in words:
            c.execute(f"SELECT Word_ID FROM word WHERE Word = '{w[0]}' AND Definition = '{w[1]}';")
            id = c.fetchone()[0]  # Get the Word_ID
            c.execute(f"INSERT INTO game_words(Game_code, Word_ID) VALUES ('{game_code}', '{id}');")

    db.commit()  # Final commit for all changes


def scramble_word(word):
    random_letters = random.sample(word, len(word))
    scrambled = ''
    for char in random_letters:
        scrambled += char
    return scrambled if scrambled != word else scramble_word(word)

def get_game_words(code, index):
    words = []
    c.execute(f"Select word, definition from game_words join word on game_words.Word_ID = word.Word_ID where Game_code = '{code}';") 
    result = c.fetchall()
    
    return (result[int(index)], len(result))

def update_completion_time(player_id, time):
    c.execute(f"UPDATE PLAYER SET Time = '{time}' WHERE Player_ID = {player_id};")
    db.commit()

def fetch_leaderboard_data(game_code):
    sql = ''
    if game_code[0] == 'S':
        sql += "SELECT P.Player_name, P.Time " 
        sql += "FROM PLAYER P " 
        sql += "JOIN GAME G ON P.Game_code = G.Game_code " 
        sql += "WHERE G.Is_classroom = FALSE "
        sql += "ORDER BY "
        sql += "    (P.Time IS NULL) ASC, "
        sql += "    P.Time ASC;     "
    else:
        sql += "SELECT DISTINCT P1.Player_name, P1.Time "    
        sql += "FROM PLAYER P1 "
        sql += f"WHERE P1.game_code = '{game_code}' " 
        sql += "ORDER BY "
        sql += "(P1.Time IS NULL) ASC,"
        sql += "P1.Time ASC;"


    c.execute(sql)

    return c.fetchall()



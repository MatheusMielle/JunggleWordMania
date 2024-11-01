def insertWords():
    sql = "INSERT INTO Word(Word, Definition, Difficulty) VALUES "

    with open("data/words_no_duplicates.txt", 'r') as file:
        for line in file:
            line = line.replace("'", "''")                
            s = line.split("|")
            word = s[0]
            defn = s[1]
            difficulty = s[2][:-1].lower()
            sql += f"('{word}', '{defn}', '{difficulty}'), "
    sql = sql[:-2]
    sql += ";"
    return sql

            

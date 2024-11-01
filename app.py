from fileInputValidator import validate
from flask import Flask, render_template, request, jsonify
from utils import *


#Start Flask
app = Flask(__name__, static_folder='./static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/SinglePlayerSettings')
def singlePlayerSettings():
    return render_template('SinglePlayerSettings.html')

@app.route('/CreateClassroom')
def createClassroom():
    return render_template('CreateClassroom.html')

@app.route("/JoinGame")
def joinGame():
    return render_template('JoinGame.html')

@app.route("/generateGameCode", methods=["POST"])
def generateGameCode():

    print("generating game code via utils func")    
    gameCode = generate_game_code(True)

    if 'file' in request.files:
        file = request.files['file']
        file = file.readlines()
        if validate(file):
            save_game_code(gameCode,True)
            create_game(game_code=gameCode, file=file)
            return jsonify({"success": True, "gameCode": gameCode})
        else:
            return jsonify({"success": False, "error": "Invalid file format. Ensure the file is in 'WORD, DEFINITION' format."})
    else:
        number_of_words = request.form.get('numberofwords')
        difficulty = request.form.get('difficulty')
        save_game_code(gameCode, True)
        create_game(game_code=gameCode,nWords=number_of_words,difficulty=difficulty)
        return jsonify({"success": True, "gameCode": gameCode})

@app.route('/ClassroomGame', methods=["POST"])
def classroomGame():
    username = request.form.get('username')
    code = request.form.get('code')
    print(f"Username: {username}\nCode: {code}")

    #Check if code is valid
    if code not in get_game_codes():
        return jsonify({"failed": True})
    
    player_id = save_player(username, code)

    return jsonify({"failed": False, "gameCode": code, "player_id" : player_id})

@app.route('/SingleGame', methods=["POST"])
def singleGame():
    code = generate_game_code(False)
    save_game_code(code, False)
    username = request.form.get('username')
    nWords = request.form.get('numberofwords')
    difficulty = request.form.get('difficulty')

    player_id  = save_player(username, code)
    create_game(game_code=code,nWords=nWords,difficulty=difficulty)

    print(f"Username: {username}\nNumber of Words: {nWords}\nDifficulty: {difficulty}")
    return render_template('Game.html', game_code = code, player_id=player_id)

@app.route('/Game/<string:game_code>/<int:player_id>')
def game(game_code, player_id):
    return render_template('Game.html', game_code = game_code, player_id=player_id)

@app.route('/get_word_definition/<string:game_code>/<int:index>')
def get_word_definition(game_code, index):
    word_defn, totalWords = get_game_words(game_code, index)
    correctWord = word_defn[0]
    definition = word_defn[1]

    return jsonify({"correct_word" : correctWord,
                    "definition" : definition,
                    "words_left" : totalWords - index,
                    "scrambled_word" : scramble_word(correctWord),
                    "total_words" : totalWords})
   
@app.route('/store_time', methods=['POST'])
def store_time():
    data = request.get_json()
    player_id = data.get('player_id')
    final_time = data.get('time')

    # Convert time from seconds to minutes:seconds format if needed
    minutes = final_time // 60
    seconds = final_time % 60
    time_str = f'{minutes:02}:{seconds:02}'

    update_completion_time(player_id=player_id, time=time_str)
    return jsonify({"message": "Time stored successfully"}), 200

@app.route('/leaderboard/<string:game_code>')
def leaderboard(game_code):
    return render_template('leaderboard.html', game_code=game_code)

@app.route('/get_leaderboard/<string:game_code>')
def get_leaderboard(game_code):
    leaderboard_data = fetch_leaderboard_data(game_code)
    response_data = [
        {
            "player_name": entry[0], 
            "time": entry[1] if entry[1] is not None else "N/A"  # Handle null time
        } 
        for entry in leaderboard_data
    ]

    return jsonify(response_data)



    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)

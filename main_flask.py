from flask import Flask, render_template, request, session
from flask_session import Session

import json
import requests
import random

app = Flask(__name__)
app.secret_key = "V@#3guru"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = r"C:\Temp"

Session(app)

wordListCreated = False

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    session["inWord"] = []
    session["new_list"] = []
    session["require"] = {}
    session["not_require"] = []
    session["somewhere"] = []
    
    return render_template("tests.html")

@app.route("/createList", methods=["POST", "GET"])
def create_wordlist():
    global wordListCreated
    
    word_len = request.form.get("word_len")
    selected_mode = request.form.get("radModeType")
    if word_len == "" or not selected_mode:
        return render_template("tests.html", MESSAGES="Please complete the DB form!", dbInputVal=word_len)
    else: pass
    
    session["word_len"] = word_len
    
    if session["word_len"] == '5':
        link = "https://raw.githubusercontent.com/cheaderthecoder/5-Letter-words/refs/heads/main/words.json"
        response = requests.get(link)
        data = response.json()
        word_list = data["words"]
        print("Using good DB")
    else:
        link = f"https://raw.githubusercontent.com/jonathanwelton/word-lists/refs/heads/main/{word_len}-letter-words.json"
        response = requests.get(link)
        word_list = response.json()
        print("using general")
    
    session["word_list"] = word_list
    session["output"] = []
    
    wordListCreated = True
    
    random_word = random.choice(session.get("word_list"))
    session["computer_output"] = random_word
    session["output"].append(random_word)
    
    return render_template("tests.html", outputArea=session.get("output"), dbInputVal=word_len)
    
@app.route("/another", methods=["GET", "POST"])
def another():
    global wordListCreated
    if wordListCreated is False:
        return render_template("tests.html", MESSAGES="Please select a Database", num_choices=session.get("choices_left"))
    else:
        pass
    
    if len(session.get("output")) == 1:
        random_word = random.choice(session["word_list"])
        session["output"][0] = random_word
        session["computer_output"] = random_word
    else:
        the_next_word = next_random_word()
        session["output"][-1] = the_next_word
        session["choices_left"] = len(session["new_list"])
    
    return render_template("tests.html", outputArea=session.get("output"), num_choices=session.get("choices_left"))

@app.route("/nextWord", methods=["POST", "GET"])
def next_word():
    user_input = request.form.get("textUserInput")
    session["output"].append(user_input)
    
    session["session_user_input"] = user_input
    session["new_list"] = []
    
    classify_input()
    filter_list()
    
    the_next_word = next_random_word()
    session["output"].append(the_next_word)
    session["choices_left"] = len(session["new_list"])
    
    return render_template('tests.html', outputArea=session.get("output"), num_choices=session["choices_left"])

def classify_input():
    user_input = session.get("session_user_input")
    computer_output = session.get("computer_output")
    
    session.setdefault("require", {})
    session.setdefault("not_require", [])
    session.setdefault("somewhere", [])
    session.setdefault("inWord", [])
    
    for i in range(len(computer_output)):
        if user_input[i].isupper():
            session["require"][i] = computer_output[i]

        elif user_input[i].islower():
            session["somewhere"].append((computer_output[i], i))

        elif user_input[i] == "-":
            if computer_output[i] not in session["inWord"]:
                session["not_require"].append(computer_output[i])
                
def filter_list():
    for word in session["word_list"]:
        
        if len(word) == len(session.get("session_user_input")):
            match = True
            
            for key, value in session["require"].items():
                if word[key] != value:
                    match = False
                    break
            
            for value in session["not_require"]:
                if value in word:
                    match = False
                    break
            
            for value, place in session["somewhere"]:
                if value not in word or word[place] == value:
                    match = False
                    break
            
            if match:
                session["new_list"].append(word)

def next_random_word():
    # set session(computer output) to new word
    next_random = random.choice(session["new_list"])
    session["computer_output"] = next_random
    return next_random
    
if __name__ == "__main__":
    app.run(debug=True)

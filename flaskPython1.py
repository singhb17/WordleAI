# from flask import Flask, render_template, request
# import requests
# import random
#
# app = Flask(__name__)
#
# word_list = []
# word_len = 0
# output = []
# lastUserInput = False
# computerOutput = ""
# userInput = ""
#
# inWord = set()
# newList = []
# require = {}
# not_require = set()
# somewhere = []
#
#
# # ---------------------- Save word len database and create word_list ---------------------------
# @app.route("/", methods=["POST", "GET"])
# def home():
#     return render_template("tests.html")
#
# @app.route("/saveDB", methods=["POST", "GET"])
# def DBReqSave():
#     wordLen = request.form.get("wordLen")
#
#     if wordLen:
#         wordLen = int(wordLen)
#         pickDatabase(wordLen)
#
#     return render_template("tests.html", dbWordLength=wordLen)
#
# def pickDatabase (wordLen):
#     global word_list
#     global word_len
#
#     word_len = wordLen
#
#     link = f"https://raw.githubusercontent.com/jonathanwelton/word-lists/refs/heads/main/{wordLen}-letter-words.json"
#     response = requests.get(link)
#     word_list = response.json()
#
# # ---------------------- Picking and Printing word ---------------------------
#
# @app.route("/pickWord", methods=["POST", "GET"])
# def printWord():
#     global output
#     global lastUserInput
#     global computerOutput
#
#
#     if len(output) > 1:
#         computerOutput = main()
#         output[-1] = computerOutput
#
#     elif len(output) == 0:
#         computerOutput = pickWord()
#         output.append(computerOutput)
#     elif len(output) == 1:
#         computerOutput = pickWord()
#         output[-1] = computerOutput
#
#     if computerOutput:
#         return render_template("tests.html", computerOutputArea = output, dbWordLength=word_len)
#     else:
#         return render_template("tests.html", computerOutputArea="No words generated!")
#
# def pickWord():
#     global word_list
#
#     if word_list:
#         return random.choice(word_list)
#     else:
#         return None
#
# # ------------------------- RESET ------------------------
#
# @app.route("/reset", methods=["POST", "GET"])
# def reset():
#     global word_list
#     global word_len
#     global output
#     global computerOutput
#     global userInput
#     global inWord, newList, require, not_require, somewhere, lastUserInput
#
#     word_list = []
#     word_len = 0
#     output = []
#     computerOutput = ""
#     userInput = ""
#     inWord = set()
#     newList = []
#     require = {}
#     not_require = set()
#     somewhere = []
#
#
#     return render_template("tests.html", randomWordDisplay="Word list reset", dbWordLength=None)
#
#
# # ------------------------- SUBMIT WORD ------------------------
#
#
# @app.route("/submitWord", methods=["POST", "GET"])
# def submitWord():
#     global word_len
#     global output
#     global lastUserInput
#     global userInput
#
#     userInput = request.form.get("textInput")
#
#     if userInput:
#         output.append(userInput)
#         nextComputerWord = main()
#         output.append(nextComputerWord) # Pick and print the next word from computer, changeable if needed in printWord function
#
#         lastUserInput = True
#         return render_template("tests.html", computerOutputArea = output, dbWordLength=output)
#
#     return None
#
#
# #! ------------------------- AI Stuff ---------------------------
#
# def classifyInput (userInput, require, not_require, somewhere, inWord):
#
#     for i in range(len(computerOutput)):
#         if userInput[i].isupper():
#             require[i] = computerOutput[i]
#
#         elif userInput[i].islower():
#             somewhere.append((computerOutput[i], i))
#
#         elif userInput[i] == "_":
#             if computerOutput[i] not in inWord:
#                 not_require.add(computerOutput[i])
#
# def filterList (word_list, newList, userInput, require, not_require, somewhere):
#
#     for word in word_list:
#
#         if len(word) == len(userInput):
#             match = True
#
#             for key, value in require.items():
#                 if word[key] != value:
#                     match = False
#                     break
#
#             for value in not_require:
#                 if value in word:
#                     match = False
#                     break
#
#             for value, place in somewhere:
#                 if value not in word or word[place] == value:
#                     match = False
#                     break
#
#             if match:
#                 newList.append(word)
#
# def finalPrint (word_list, newList, computerInput):
#     if newList != []:
#         computerInput = random.choice(newList)
#         print(computerInput)
#     else:
#         computerInput = random.choice(word_list)
#         print(f"No words found, choosing from big list: {computerInput}")
#
#     return computerInput
#
# def main():
#
#     global inWord
#     global newList
#     global require
#     global not_require
#     global somewhere
#
#     global userInput
#     global computerOutput
#     global word_list
#     global lastUserInput
#
#     newList = []
#     inWord = set(char.lower() for char in userInput if char.isalpha())
#
#     classifyInput(userInput, require, not_require, somewhere, inWord)
#     filterList(word_list, newList, userInput, require, not_require, somewhere)
#     computerOutput = random.choice(newList) if newList else random.choice(word_list)
#
#     return computerOutput
#
# if __name__ == '__main__':
#     app.run(debug=True)
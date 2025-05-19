import requests
import random

wordLen = 0;

def pickDatabase ():
    global wordLen
    
    print("5-letter-OLD: A")
    print("5-letter-NEW: B")
    print("10-letter-GH: C")
    print("Custom Length: D")
    selectDB = input("Choose a DB: ")
    print("****************************")
    
    fiveLetter_fifteenThou = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    fiveLetter_fiveThou = "https://raw.githubusercontent.com/cheaderthecoder/5-Letter-words/refs/heads/main/words.json"
    tenLetter = "https://raw.githubusercontent.com/jonathanwelton/word-lists/refs/heads/main/10-letter-words.json"
    
    if selectDB == "A":
        response = requests.get(fiveLetter_fifteenThou)
        word_list = response.text.splitlines()
        wordLen = 5
        
    elif selectDB == "B":
        response = requests.get(fiveLetter_fiveThou)
        data = response.json()
        word_list = data["words"]
        wordLen = 5
        
    elif selectDB == "C":
        response = requests.get(tenLetter)
        word_list = response.json()
        wordLen = 10
        
    elif selectDB == "D":
        x = int(input("Enter length of word (integer only): "))
        
        if (x < 1 or x > 31 or x == 20):
            print("Invalid input, restarting... Please pick DB again!")
            print("****************************")
            return pickDatabase()
        
        flexible = f"https://raw.githubusercontent.com/jonathanwelton/word-lists/refs/heads/main/{x}-letter-words.json"
        response = requests.get(flexible)

        word_list = response.json()
        wordLen = x
    
    return word_list, wordLen

def chooseMode ():
    global fromMiddle
    print("From Scratch: A")
    print("From middle: B")
    chooseMode = input("Choose a Mode: ")
    print("****************************")
    
    if chooseMode == "A":
        return 'A'
    elif chooseMode == "B":
        # startFromMiddle(newList, require, not_require, somewhere, inWord, word_list, wordLen)
        return 'B'

def startFromMiddle (newList, require, not_require, somewhere, inWord, word_list, wordLen):

    while True:
        numWords = input("How many times guessed already? ")
        if numWords.isdigit() == False:
            print("Oops, that was not a number. Try again please\n")
        else:
            numWords = int(numWords)
            break
        
    newList.clear()
    
    for _ in range(numWords):
        while True:
            wordInput = input("Enter a word and feedback with a space: ")
            computerInput, userInput = wordInput.split()
            if len(userInput) != wordLen or len(computerInput) != wordLen:
                print(f"Oops, your feedback was not {wordLen} letters long. Try again please\n")
            else:
                break
        
        for i, fb in enumerate(userInput):
            if fb.isalpha():
                inWord.add(computerInput[i].lower())
                
        classifyInput(computerInput, userInput, require, not_require, somewhere, inWord)
        
    filterList(word_list, newList, userInput, require, not_require, somewhere)
    return newList
    
def inputHandling (word_list, newList, computerInput, require, not_require, somewhere, wordLen):
    
    userInput = input("Feedback: ")
    print("**************")
    
    # Some error or bug down here preventing use of another right after restart
    # Fixed now. made all condition inside a while loop
    while True:
        if userInput == "another":
            if newList != []:
                computerInput = random.choice(newList)
            else:
                computerInput = random.choice(word_list)

            print(computerInput)
            userInput = input("Feedback: ")
            print("**************")
            
        elif userInput == "restart":
            require.clear()
            not_require.clear()
            somewhere.clear()
            newList.clear()
            
            print("**************")
            computerInput = random.choice(word_list)
            print(computerInput)
            userInput = input("Feedback: ")
            print("**************")
            
        elif userInput == "change DB":
            main()
            
        elif userInput == "exit":
            pass
        
        elif len(userInput) != wordLen:
            print(f"Oops, your feedback was not {wordLen} letters long")
            print("Try Again please: ")
            
            userInput = input("Feedback: ")
            print("**************")
        
        else:
            break
            
    return userInput, computerInput

def classifyInput (computerInput, userInput, require, not_require, somewhere, inWord):
    
    for i in range(len(computerInput)):   
        if userInput[i].isupper():
            require[i] = computerInput[i]
            
        elif userInput[i].islower():
            somewhere.append((computerInput[i], i))
            
        elif userInput[i] == "_":
            if computerInput[i] not in inWord:
                not_require.add(computerInput[i])

def filterList (word_list, newList, userInput, require, not_require, somewhere):
    
    for word in word_list:
        
        if len(word) == len(userInput):
            match = True

            for key, value in require.items():
                if word[key] != value:
                    match = False
                    break

            for value in not_require:
                if value in word:
                    match = False
                    break
            
            for value, place in somewhere:
                if value not in word or word[place] == value:
                    match = False
                    break
                
            if match:
                newList.append(word)
        
def finalPrint (word_list, newList, computerInput):
    if len(newList) <= 12 and len(newList) != 1:
        print(newList)
        
    elif len(newList) == 1:
        print("Last option... ")

    if newList != []:
        computerInput = random.choice(newList)
        print(computerInput)
    else:
        computerInput = random.choice(word_list)
        print(f"No words found, choosing from big list: {computerInput}")
        
    return computerInput

def main ():
    
    inWord = set()
    newList = []
    require = {}
    not_require = set()
    somewhere = []    
    word_list, wordLen = pickDatabase()
    
    mode = chooseMode()
    
    if mode == 'A':
        computerInput = random.choice(word_list)
        print(computerInput)
    elif mode == 'B':
        newList = startFromMiddle(newList, require, not_require, somewhere, inWord, word_list, wordLen)
        computerInput = random.choice(newList) if newList else print("Bruh") and random.choice(word_list)
        print(computerInput)
    else:
        print("Invalid mode selected, starting again...")
        print("**************")
        return
    
    while True:
        userInput, computerInput = inputHandling(word_list, newList, computerInput, require, not_require, somewhere, wordLen)
        if userInput == "exit":
            break
        
        newList = []
        inWord = set(char.lower() for char in userInput if char.isalpha())
        
        classifyInput(computerInput, userInput, require, not_require, somewhere, inWord)
        filterList(word_list, newList, userInput, require, not_require, somewhere)
        computerInput = finalPrint(word_list, newList, computerInput)
        
main()
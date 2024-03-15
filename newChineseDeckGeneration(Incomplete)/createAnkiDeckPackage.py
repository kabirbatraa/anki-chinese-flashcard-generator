
# write the name of the vocab list here: (might only work with txt files)
# Example: vocabListFileName = "Lesson 1.txt"

vocabListFileName = "L9 Vocab List.docx.txt"
vocabListFileName = "testList.txt"

import requests
import genanki

    
def getStrokeData(character = "我"):
    # if character in "（）":
    #     # skip because its just a parenthesis
    #     return None

    url = f"https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{character}.json"
    response = requests.get(url)
    jsonData = response.content
    jsonData = jsonData.decode()

    # if its not a chinese character, then returns None
    if "Couldn't find the requested file" in jsonData:
        print("could not find file for " + character + "; skipping this character")
        return None
    return jsonData

# test
# print("testing getStrokeData", getStrokeData("（"))

vocabListFile = open(vocabListFileName, "r", encoding="utf8") # "r" means read
# print(file.read())

# 'deckname': [('front', 'back'), ('front', 'back'), ...)]
decks = {}
writeToFiles = False

# new file is created whenever a new section is reached in the file
ankiDeckFile = None
currentDeckName = None

# each line has a new line at the end of it already
for line in vocabListFile:

    # if a line is empty, then skip it 
    if line == "\n": 
        # print("empty line")
        continue
    
    # split the line into parts by semicolon or colon
    chineseSemicolon = "；"
    normalSemicolon = ";"
    colon = ":"

    # replace occurences of colon or chinese semicolon with normal semicolon
    line = line.replace(chineseSemicolon, normalSemicolon)
    line = line.replace(colon, normalSemicolon)
    # then split by semicolon
    lineParts = line.split(normalSemicolon)

    # strip/trim off any learning or trailing whitespace from each part
    for i in range(len(lineParts)):
        lineParts[i] = lineParts[i].strip()


    
    # if a line does not have any semicolons, it must be the title of a new deck
    if len(lineParts) == 1:
        deckName = lineParts[0]
        # deckName = deckName.replace(' ', ' ') # attempt to replace chinese space with regular space
        print("New Deck:", deckName)

        # if we already have a file open, then close it before creating a new file
        if currentDeckName != None:
            if writeToFiles: ankiDeckFile.close()
        
        # create a new file for this new deck
        if writeToFiles: ankiDeckFile = open(deckName + ".txt", "w", encoding="utf8")
        currentDeckName = deckName
        
        continue

    # otherwise, this is a vocab term
    vocabTerm = lineParts
    
    # print(vocabTerm)
    hanzi = vocabTerm[0]
    print('adding', hanzi)
    pinyin = vocabTerm[1]
    definition = vocabTerm[2]
    examplesExist = True
    if (len(vocabTerm) == 5):
        exampleChinese = vocabTerm[3]
        exampleEnglish = vocabTerm[4] # chinese example translated into english
        # examplesExist = True
    else:
        examplesExist = False
        print("this term does not have examples")
    # print("hanzi:", hanzi)
    # print("pinyin:", pinyin)


    # if no file was opened, then this vocab term comes before something like "Text 1" to label the deck
    if currentDeckName == None:
        if writeToFiles: ankiDeckFile = open("NoDeckName.txt", 'w', encoding="utf8")
        currentDeckName = "NoDeckName"
        


    # format for hanzi writer + my template
    def getCardFrontBack():

        front = f"{definition}"
        if examplesExist: front += f"<br>(phrases: {exampleEnglish})"

        back = f"{hanzi} {pinyin}"
        if examplesExist: back += f"<br>(phrases: {exampleChinese})"
        back += "<br>"

        # format for the back side:
        # <div id="hanzi" style="display:none">我是钢琴</div>
        # <img src="我.js" style="display:none">
            # for each hanzi

        back += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'
        # add the hanzi to the front too so we can potentially add hanzi writer quiz
        front += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'

        # add the stroke order data in an invisible div
        for character in hanzi:
            # no need to add the dummy image to trick anki into thinking the character js is a dependency
            # back += f'<img src="{character}.js" style="display:none">'
            # downloadStrokeData(character)

            strokeJsonData = getStrokeData(character)
            if strokeJsonData == None: continue
            back += f'<div id="{character}" style="display:none">{strokeJsonData}</div>'
        
        return (front, back)
        # ankiDeckFile.write(front + ";" + back + "\n")

    # writeToFileHanziWriterFormat()
    front, back = getCardFrontBack()
    if writeToFiles: ankiDeckFile.write(front + ";" + back + "\n")
    if (currentDeckName not in decks): decks[currentDeckName] = []
    decks[currentDeckName].append((front, back))




# decks dictionary
# each deck should contain a list of tuples: front and back of card




import genanki 

# def convertTextFileToDeck(textFileName):
#     open(textFile)

# how to escape html:
# fields=[html.escape(f) for f in ['AT&T was originally called', 'Bell Telephone Company']]


# from anki ?
# Card ID	1710460837938
# Note ID	1710460837937

# https://github.com/AnKing-VIP/advanced-browser
# https://ankiweb.net/shared/info/874215009
# use this addon to get internal information on cards
# including the note type id aka model id
# this will allow me to overwrite the old model on lesson 8
# (because it will have the same id)

# old model id: 1607392319
# updating the model id will create a new model (card template)

# the model id i will use for now: 1956882460
# text1: 1567115450
# text2: 1705746358
# supplementary: 1152996867
# basic hanzi: 1085417380

# how to create a model:
my_model = genanki.Model(
    1607392310,
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css=\
""".card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}"""
)
# use a unique model id:
# import random; random.randrange(1 << 30, 1 << 31)
# and hardcode it into your Model definition.

# create a new note:
my_note = genanki.Note(
    model=my_model, 
    fields=["Capital of Argentina", "Buenos Aires"]
)


# make a deck
my_deck = genanki.Deck(2059400110, "Country Capitals")

my_deck.add_note(my_note)
genanki.Package(my_deck).write_to_file('output.apkg')
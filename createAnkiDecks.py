# write the name of the vocab list here:
# Example: vocabListFileName = "Lesson 1.txt"
vocabListFileName = "L8 Vocab List.txt"

vocabListFile = open(vocabListFileName, "r", encoding="utf8") # "r" means read
# print(file.read())

# new file is created whenever a new section is reached in the file
ankiDeckFile = None

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
        print("New Deck:", deckName)

        # if we already have a file open, then close it before creating a new file
        if ankiDeckFile != None:
            ankiDeckFile.close()
        
        # create a new file for this new deck
        ankiDeckFile = open(deckName + ".txt", "w", encoding="utf8")
        continue

    # otherwise, this is a vocab term
    vocabTerm = lineParts

    

    hanzi = vocabTerm[0]
    pinyin = vocabTerm[1]
    definition = vocabTerm[2]
    if (len(vocabTerm) == 5):
        exampleChinese = vocabTerm[3]
        exampleEnglish = vocabTerm[4] # chinese example translated into english
    else:
        print("this term does not have examples")
    print(vocabTerm)
    print("hanzi:", hanzi)
    print("pinyin:", pinyin)
    # print(lineParts)


    # now write the vocab term to the file

    # if no file was opened, then this vocab term comes before something like "Text 1" to label the deck
    if ankiDeckFile == None:
        ankiDeckFile = open("NoDeckName.txt", 'w', encoding="utf8")
    
    front = f"{definition} <br>(phrases: {exampleEnglish})"
    back = f"{hanzi} {pinyin} <br>(phrases: {exampleChinese})"
    ankiDeckFile.write(front + ";" + back + "\n")



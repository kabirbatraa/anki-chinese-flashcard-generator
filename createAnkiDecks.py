# write the name of the vocab list here:
# Example: vocabListFileName = "Lesson 1.txt"
vocabListFileName = "L8 Vocab List.txt"



# if beautifulsoup4 or requests don't exist, then 
# use the command: pip install beautifulsoup4, or pip install requests 
# import requests
# from bs4 import BeautifulSoup

# url = "http://www.strokeorder.info/mandarin.php?q=我"
# url = url.encode('utf-8')
# print(url)
# response = requests.get(url)
# html_content = response.content

# print(html_content)

# soup = BeautifulSoup(html_content, "html.parser")
# img_tags = soup.find_all("img")

# image_urls = []
# for img_tag in img_tags:
#     image_url = img_tag.get("src")
#     if image_url:
#         image_urls.append(image_url)

# for image_url in image_urls:
#     image_response = requests.get(image_url)
#     with open(f"image_{image_urls.index(image_url)}.jpg", "wb") as f:
#         f.write(image_response.content)


import requests

def downloadStrokeData(character = "我"):
    if character in "（）":
        # skip because its just a parenthesis
        return

    url = f"https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{character}.json"
    response = requests.get(url)
    jsonData = response.content
    # with open(f'jsonStrokeData/stroke_data_{character}.json', 'wb') as f:
    #     f.write(jsonData)
    
    with open(f'jsonStrokeData/stroke_data_{character}.js', 'wb') as f:
        jsonData = jsonData.decode()
        jsonData = f'characterData["{character}"] = ' + jsonData
        jsonData = jsonData.encode()
        f.write(jsonData)
    
def getStrokeData(character = "我"):
    if character in "（）":
        # skip because its just a parenthesis
        return None

    url = f"https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{character}.json"
    response = requests.get(url)
    jsonData = response.content
    jsonData = jsonData.decode()
    return jsonData

    

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

    
    # print(vocabTerm)
    hanzi = vocabTerm[0]
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
    if ankiDeckFile == None:
        ankiDeckFile = open("NoDeckName.txt", 'w', encoding="utf8")


    # now write the vocab term to the file


    # not using this right now
    def writeToFileStrokeOrderInfoFormat():
        # get the image associated with each hanzi character
        hanziGifImageTags = []

        firstCharacter = hanzi[0]
        
        # the stroke order website seems to not be working


        hanziGifImageTags.append('<img src="apple.jpg">')


        
        
        front = f"{definition}"
        if examplesExist: front += f"<br>(phrases: {exampleEnglish})"
        back = f"{hanzi} {pinyin}"
        if examplesExist: back += f"<br>(phrases: {exampleChinese})"
        back += "<br>"
        for imageTag in hanziGifImageTags:
            back += f'{imageTag}'
        
        ankiDeckFile.write(front + ";" + back + "\n")
    


    # format for hanzi writer + my template
    def writeToFileHanziWriterFormat():

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
        for character in hanzi:
            # no need to add the dummy image to trick anki into thinking the character js is a dependency
            # back += f'<img src="{character}.js" style="display:none">'
            # downloadStrokeData(character)

            strokeJsonData = getStrokeData(character)
            if strokeJsonData == None: continue
            back += f'<div id="{character}" style="display:none">{strokeJsonData}</div>'
        
        ankiDeckFile.write(front + ";" + back + "\n")


    writeToFileHanziWriterFormat()




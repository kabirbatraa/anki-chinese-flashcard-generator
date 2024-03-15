# anki-chinese-flashcard-generator

Takes in vocab list from chinese class and generates anki deck.

### Features:

- Custom HTML/CSS/Javascript template uses the HanziWriter javascript library to render Chinese flashcards with stroke order.
- Parses the vocab list text file, downloads HanziWriter stroke order data, and generates the front and back of flashcards (including examples) in a format compatible with my flashcard template.
- Uses genanki library to package decks of cards into an anki package.

## How to use
1. Download this repository.
2. Add vocab list as a text file into the folder.
3. Go into `createAnkiDeckPackage.py` and edit the variables up top.
   - `outerDeckName`: will be used to name the deck containing the subdecks
   - `vocabListFileName`: name of the vocab list text file
4. Run `python createAnkiDeckPackage.py` in the terminal. 
   - Make sure python is installed.
   - You will need to install libraries: requests, genanki, random.
   - use pip install \<library name\>.
5. That's it! the apkg file will be created for you!

I recommend using 



import genanki 


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
# testing 1607392310
# testing None
# updating the model id will create a new model (card template)

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
# old deck id:2059400110
my_deck = genanki.Deck(2059400110, "Country Capitals")

my_deck.add_note(my_note)
genanki.Package(my_deck).write_to_file('output.apkg')
import json

data = json.load(open("data.json"))

def translate(w):

    if w in data:
        return data[w]
    else:
        return "The word is not in the dictionary"

word = input("Write a word to translate: ")

print (translate(word))

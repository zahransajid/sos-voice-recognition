import spacy
from fuzzywuzzy import process

nlp = spacy.load("en_core_web_sm")

# phrases
predefined_phrases = [
    "can i get some help",
    "example",
    "example",
    "call the doctor",
    "i need immediate attention"
]

def extract_nouns(phrase):
    doc = nlp(phrase)
    nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    return nouns

def get_closest_match(phrase, phrase_list, threshold=80):
    
    input_nouns = extract_nouns(phrase)

    filtered_phrases = []
    for predefined_phrase in phrase_list:
        predefined_nouns = extract_nouns(predefined_phrase)
        if any(noun in predefined_nouns for noun in input_nouns):
            filtered_phrases.append(predefined_phrase)

    if not filtered_phrases:
        filtered_phrases = phrase_list

    closest_match, score = process.extractOne(phrase, filtered_phrases)
    
    return closest_match, score


if __name__ == '__main__':
    # Example input

    input_phrase = "i need the doctor"

    # Find the closest matching phrase
    closest_match, _ = get_closest_match(input_phrase, predefined_phrases)
    print(f"Closest match: {closest_match}")

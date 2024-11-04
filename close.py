import spacy
from fuzzywuzzy import process

nlp = spacy.load("en_core_web_sm")

predefined_phrases = [
    "can i get some help",
    "example",
    "example",
    "call the doctor",
    "i need immediate attention"
]

def extract_nouns(phrase):
    """Extracts nouns from a given phrase using spaCy."""
    doc = nlp(phrase)
    nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    return nouns

def get_closest_match(phrase, phrase_list, threshold=80, boost_score=20):
    input_nouns = extract_nouns(phrase)

    boosted_matches = []

    for predefined_phrase in phrase_list:
        closest_match, score = process.extractOne(phrase, [predefined_phrase])

        predefined_nouns = extract_nouns(predefined_phrase)

        if any(noun in predefined_nouns for noun in input_nouns):
            score += 50 

        boosted_matches.append((predefined_phrase, score))

    best_match = max(boosted_matches, key=lambda x: x[1])
    return best_match

# Example
if __name__ == '__main__':
    input_phrase = "i need the doctor"

    closest_match = get_closest_match(input_phrase, predefined_phrases)
    print(f"Closest match: {closest_match}")

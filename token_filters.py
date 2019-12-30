import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_punctuation_tokens(tokens):
    return [t for t in tokens if t not in string.punctuation]


retain_stops = {'i', 'me', 'my', 'myself', 'you', 'your', 'yours', 'yourself', 'he', 'him', 'his', 'himself', 'ma'}
stop_words = set(stopwords.words('english')).difference(retain_stops)
cap_stop_words = [word.capitalize() for word in stop_words]


def remove_stopwords(words):
    lower_stops_removed = [w for w in words if w not in stop_words]
    all_stops_removed = [w for w in lower_stops_removed if w not in cap_stop_words]
    return all_stops_removed


def text_to_words_without_stopwords(text):
    return remove_stopwords(remove_punctuation_tokens(tokenize(text)))


def split_token_by_punctuation(token):
    if len(token) <= 2:
        return [token]
    prefix = ''
    suffix = ''
    if not token[0].isalnum():
        prefix = token[0]
        token = token[1:]
    if not token[-1].isalnum():
        suffix = token[-1]
        token = token[:-1]
    return [prefix, token, suffix]


def tokenize(text):
    tokens = word_tokenize(text)
    new_tokens = []
    for token in tokens:
        new_tokens += split_token_by_punctuation(token)
    return new_tokens


STOP_PHRASES = ['as well as', 'as well']


def remove_stop_phrases(sentence):
    for phrase in STOP_PHRASES:
        sentence = sentence.replace(phrase, '')
    return sentence


PHRASE_MAP = [
    {"regex": r'[Ww]ork(?:ing|s)? without attachment[s]?(?: to(?:ward[s]?)? outcome[s]?)?',
     "phrase": 'karmayOga_a_defn'},
    {"regex": r'[Ww]ork(?:ing|s)? without being driven(?: by desire[s]?)?',
     "phrase": 'karmayOga_a_defn'}
]


# TODO: this is not yet used. Tokenize a phrase from a sentence before tokenizing the words
def catch_phrases(text):
    for phrase in PHRASE_MAP:
        text = re.sub(phrase["regex"], phrase["phrase"], text)
    return text


def significant_words(sentence):
    return remove_stopwords(
                remove_punctuation_tokens(
                  tokenize(
                    remove_stop_phrases(sentence))))

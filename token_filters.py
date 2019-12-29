import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_punctuations(tokens):
    return [t for t in tokens if t not in string.punctuation]


retain_stops = {'i', 'me', 'my', 'myself', 'you', 'your', 'yours', 'yourself', 'he', 'him', 'his', 'himself', 'ma'}
stop_words = set(stopwords.words('english')).difference(retain_stops)
cap_stop_words = [word.capitalize() for word in stop_words]


def remove_stopwords(words):
    lower_stops_removed = [w for w in words if w not in stop_words]
    all_stops_removed = [w for w in lower_stops_removed if w not in cap_stop_words]
    return all_stops_removed


def text_to_words_without_stopwords(text):
    return remove_stopwords(remove_punctuations(tokenize(text)))


def tokenize(text):
    return word_tokenize(text)


STOP_PHRASES = ['as well as', 'as well']


def remove_stop_phrases(sentence):
    for phrase in STOP_PHRASES:
        sentence = sentence.replace(phrase, '')
    return sentence


def significant_words(sentence):
    return remove_stopwords(
                remove_punctuations(
                  tokenize(
                    remove_stop_phrases(sentence))))

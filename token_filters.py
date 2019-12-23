import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_punctuations(tokens):
    return [t for t in tokens if t not in string.punctuation]


def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [w for w in words if w not in stop_words]


def text_to_words_without_stopwords(text):
    return remove_stopwords(remove_punctuations(tokenize(text)))


def lower_first_char_and_join(sentence_list):
    joined_text = ''
    for sentence in sentence_list:
        sentence = sentence.strip()
        if len(sentence) > 0:
            """Remove initial caps"""
            sentence = sentence[0].lower() + sentence[1:]
            joined_text += sentence + ' '
    return joined_text


def tokenize(text):
    sentence_starters = '?!\'\"'
    for starter in sentence_starters:
        text = text.replace(starter, '.')
    sentence_list = text.split('.')
    text = lower_first_char_and_join(sentence_list)
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
